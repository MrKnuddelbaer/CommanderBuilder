"""CommanderBuilder – FastAPI-App (API + statisches Frontend)."""
import hashlib
import hmac
import json
import os
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import advisor, analysis, collectr, scryfall
from .db import db, init, now

APP_PASSWORD = os.environ.get("APP_PASSWORD", "")
SECRET = os.environ.get("SESSION_SECRET", APP_PASSWORD or "dev")
STATIC = Path(__file__).parent.parent / "static"
PRECONS = Path(__file__).parent / "precons"

app = FastAPI(title="CommanderBuilder")
init()


# ---------- Login (ein Passwort, Cookie) ----------
def _token():
    return hmac.new(SECRET.encode(), b"commanderbuilder", hashlib.sha256).hexdigest()


@app.middleware("http")
async def auth(request: Request, call_next):
    p = request.url.path
    if APP_PASSWORD and p.startswith("/api/") and p not in ("/api/login", "/api/status"):
        if request.cookies.get("cb_session") != _token():
            return JSONResponse({"detail": "Nicht angemeldet"}, status_code=401)
    return await call_next(request)


class Login(BaseModel):
    password: str


@app.post("/api/login")
def login(body: Login):
    if APP_PASSWORD and not hmac.compare_digest(body.password, APP_PASSWORD):
        raise HTTPException(401, "Falsches Passwort")
    resp = JSONResponse({"ok": True})
    resp.set_cookie("cb_session", _token(), httponly=True, samesite="lax", max_age=60 * 60 * 24 * 365, secure=bool(APP_PASSWORD))
    return resp


@app.get("/api/status")
def status(request: Request):
    return {
        "auth_required": bool(APP_PASSWORD),
        "logged_in": not APP_PASSWORD or request.cookies.get("cb_session") == _token(),
        "ai": bool(advisor.ANTHROPIC_KEY),
        "models": {"default": advisor.MODEL_DEFAULT, "deep": advisor.MODEL_DEEP},
    }


# ---------- Hilfsfunktionen ----------
def ownership(exclude_deck=None) -> tuple[dict, dict]:
    """({oracle-name-lower: qty}, {oracle-name-lower: [Decknamen]})"""
    with db() as con:
        owned = {}
        for r in con.execute("SELECT name, SUM(qty) q FROM collection WHERE name IS NOT NULL GROUP BY lower(name)"):
            owned[r["name"].lower()] = r["q"]
        used = {}
        q = "SELECT d.name dn, dc.name cn FROM deck_cards dc JOIN decks d ON d.id=dc.deck_id WHERE dc.section!='maybe'"
        args = ()
        if exclude_deck is not None:
            q += " AND d.id != ?"
            args = (exclude_deck,)
        for r in con.execute(q, args):
            used.setdefault(r["cn"].lower(), []).append(r["dn"])
    return owned, used


def _deck_row(deck_id):
    with db() as con:
        d = con.execute("SELECT * FROM decks WHERE id=?", (deck_id,)).fetchone()
        if not d:
            raise HTTPException(404, "Deck nicht gefunden")
        cards = [dict(r) for r in con.execute("SELECT name, qty, section, physical FROM deck_cards WHERE deck_id=?", (deck_id,))]
    return dict(d), cards


async def _resolve_list(entries: list[dict]) -> tuple[list[dict], list[str]]:
    """Namen aus Textlisten auf Oracle-Namen abbilden."""
    found, nf = await scryfall.get_cards([e["name"] for e in entries])
    out = []
    for e in entries:
        c = found.get(e["name"])
        if c:
            out.append({**e, "name": c["name"]})
    return out, nf


def _save_cards(con, deck_id, entries, physical=False):
    for e in entries:
        con.execute(
            "INSERT INTO deck_cards(deck_id, name, qty, section, physical) VALUES (?,?,?,?,?) "
            "ON CONFLICT(deck_id, name, section) DO UPDATE SET qty=qty+excluded.qty",
            (deck_id, e["name"], e["qty"], e["section"], int(physical)),
        )


async def _full_deck(deck_id):
    deck, rows = _deck_row(deck_id)
    found, _ = await scryfall.get_cards([r["name"] for r in rows])
    owned, used = ownership(exclude_deck=deck_id)
    cards = []
    for r in rows:
        c = dict(found.get(r["name"]) or {"name": r["name"], "type_line": "?", "oracle_text": ""})
        c.update(qty=r["qty"], section=r["section"])
        key = c["name"].lower()
        basic = key in analysis.BASICS
        c["physical"] = bool(r.get("physical"))
        c["owned"] = basic or c["physical"] or owned.get(key, 0) >= 1
        c["owned_qty"] = owned.get(key, 0)
        c["in_decks"] = used.get(key, [])
        cards.append(c)
    return deck, cards


# ---------- Sammlung ----------
@app.post("/api/collection/import")
async def import_collection(file: UploadFile = File(...)):
    text = (await file.read()).decode("utf-8", errors="replace")
    rows = collectr.parse(text)
    if not rows:
        raise HTTPException(400, "Keine Magic-Karten in der Datei gefunden (Collectr-CSV-Export?)")
    first = [r["candidates"][0] for r in rows]
    found, _ = await scryfall.get_cards(first, fuzzy_fallback=False)
    retry = [c for r in rows if r["candidates"][0] not in found for c in r["candidates"][1:]]
    found2, _ = await scryfall.get_cards(retry) if retry else ({}, [])
    found.update(found2)
    unresolved = []
    with db() as con:
        con.execute("DELETE FROM collection")
        for r in rows:
            card = next((found[c] for c in r["candidates"] if c in found), None)
            if not card:
                unresolved.append(r["raw_name"])
            con.execute(
                "INSERT INTO collection(raw_name, name, set_name, qty, finish, price_usd, imported_at) VALUES (?,?,?,?,?,?,?)",
                (r["raw_name"], card["name"] if card else None, r["set_name"], r["qty"], r["finish"], r["price_usd"], now()),
            )
    return {"imported": len(rows), "cards": sum(r["qty"] for r in rows), "unresolved": unresolved}


@app.get("/api/collection")
async def get_collection(q: str = "", color: str = "", only_free: bool = False):
    with db() as con:
        rows = [dict(r) for r in con.execute(
            "SELECT name, SUM(qty) qty, GROUP_CONCAT(DISTINCT set_name) sets FROM collection WHERE name IS NOT NULL GROUP BY name ORDER BY name")]
        unresolved = [r["raw_name"] for r in con.execute("SELECT raw_name FROM collection WHERE name IS NULL")]
    data = scryfall.cached_any([r["name"] for r in rows])
    _, used = ownership()
    out = []
    for r in rows:
        c = data.get(r["name"], {})
        if q and q.lower() not in r["name"].lower() and q.lower() not in (c.get("type_line") or "").lower():
            continue
        if color and not set(c.get("color_identity", [])) <= set(color.upper()):
            continue
        in_decks = used.get(r["name"].lower(), [])
        if only_free and len(in_decks) >= r["qty"]:
            continue
        out.append({**r, "type_line": c.get("type_line"), "eur": c.get("eur"), "color_identity": c.get("color_identity", []),
                    "image_small": c.get("image_small"), "image": c.get("image"), "in_decks": in_decks})
    total_eur = round(sum((x["eur"] or 0) * x["qty"] for x in out), 2)
    return {"cards": out, "unresolved": unresolved, "total_eur": total_eur}


# ---------- Decks ----------
class NewDeck(BaseModel):
    name: str
    commander: str = ""
    bracket: int = 2
    budget_eur: float = 25
    decklist: str = ""
    physical: bool = False   # True = ich besitze das Deck so (z. B. Precon)


@app.get("/api/decks")
def list_decks():
    with db() as con:
        return [dict(r) for r in con.execute(
            "SELECT d.*, (SELECT SUM(qty) FROM deck_cards WHERE deck_id=d.id AND section!='maybe') cards FROM decks d ORDER BY d.id DESC")]


@app.post("/api/decks")
async def create_deck(body: NewDeck):
    entries = collectr.parse_decklist(body.decklist) if body.decklist else []
    if body.commander and not any(e["section"] == "commander" for e in entries):
        entries.insert(0, {"name": body.commander, "qty": 1, "section": "commander"})
    resolved, nf = await _resolve_list(entries)
    cmd = next((e["name"] for e in resolved if e["section"] == "commander"), body.commander)
    with db() as con:
        cur = con.execute("INSERT INTO decks(name, commander, bracket, budget_eur, created_at) VALUES (?,?,?,?,?)",
                          (body.name, cmd, body.bracket, body.budget_eur, now()))
        _save_cards(con, cur.lastrowid, resolved, physical=body.physical)
    return {"id": cur.lastrowid, "not_found": nf}


@app.get("/api/precons")
def list_precons():
    return [p.stem for p in PRECONS.glob("*.txt")]


@app.post("/api/precons/{slug}")
async def load_precon(slug: str, owned: bool = True):
    path = PRECONS / f"{slug}.txt"
    if not path.exists():
        raise HTTPException(404, "Precon unbekannt")
    text = path.read_text()
    title = text.splitlines()[0].lstrip("# ").split(" (")[0]
    return await create_deck(NewDeck(name=title, bracket=2, budget_eur=25, decklist=text, physical=owned))


class DeckPatch(BaseModel):
    name: str | None = None
    bracket: int | None = None
    budget_eur: float | None = None
    notes: str | None = None


@app.patch("/api/decks/{deck_id}")
def patch_deck(deck_id: int, body: DeckPatch):
    fields = {k: v for k, v in body.model_dump().items() if v is not None}
    if fields:
        with db() as con:
            con.execute(f"UPDATE decks SET {', '.join(k + '=?' for k in fields)} WHERE id=?", (*fields.values(), deck_id))
    return {"ok": True}


@app.delete("/api/decks/{deck_id}")
def delete_deck(deck_id: int):
    with db() as con:
        con.execute("DELETE FROM deck_cards WHERE deck_id=?", (deck_id,))
        con.execute("DELETE FROM history WHERE deck_id=?", (deck_id,))
        con.execute("DELETE FROM decks WHERE id=?", (deck_id,))
    return {"ok": True}


@app.get("/api/decks/{deck_id}")
async def get_deck(deck_id: int):
    deck, cards = await _full_deck(deck_id)
    ana = analysis.analyse(deck, cards)
    with db() as con:
        hist = [dict(r) for r in con.execute("SELECT action, created_at FROM history WHERE deck_id=? ORDER BY id DESC LIMIT 30", (deck_id,))]
    return {"deck": deck, "cards": cards, "analysis": ana, "history": hist}


class CardOp(BaseModel):
    name: str
    section: str = "main"
    qty: int = 1


@app.post("/api/decks/{deck_id}/cards")
async def add_card(deck_id: int, body: CardOp):
    resolved, nf = await _resolve_list([body.model_dump()])
    if not resolved:
        raise HTTPException(404, f"Karte nicht gefunden: {body.name}")
    with db() as con:
        _save_cards(con, deck_id, resolved)
        con.execute("INSERT INTO history(deck_id, action, created_at) VALUES (?,?,?)", (deck_id, f"+ {resolved[0]['name']}", now()))
    return {"ok": True, "name": resolved[0]["name"]}


@app.delete("/api/decks/{deck_id}/cards")
def remove_card(deck_id: int, name: str, section: str = "main"):
    with db() as con:
        con.execute("UPDATE deck_cards SET qty=qty-1 WHERE deck_id=? AND name=? AND section=?", (deck_id, name, section))
        con.execute("DELETE FROM deck_cards WHERE qty<=0")
        con.execute("INSERT INTO history(deck_id, action, created_at) VALUES (?,?,?)", (deck_id, f"− {name}", now()))
    return {"ok": True}


class Swap(BaseModel):
    out: str
    into: str


@app.post("/api/decks/{deck_id}/swap")
async def swap(deck_id: int, body: Swap):
    resolved, _ = await _resolve_list([{"name": body.into, "qty": 1, "section": "main"}])
    if not resolved:
        raise HTTPException(404, f"Karte nicht gefunden: {body.into}")
    with db() as con:
        row = con.execute("SELECT section FROM deck_cards WHERE deck_id=? AND name=? AND section!='commander'", (deck_id, body.out)).fetchone()
        if not row:
            raise HTTPException(400, f"{body.out} ist nicht im Deck")
        con.execute("UPDATE deck_cards SET qty=qty-1 WHERE deck_id=? AND name=? AND section=?", (deck_id, body.out, row["section"]))
        con.execute("DELETE FROM deck_cards WHERE qty<=0")
        _save_cards(con, deck_id, resolved)
        con.execute("INSERT INTO history(deck_id, action, created_at) VALUES (?,?,?)", (deck_id, f"{body.out} → {resolved[0]['name']}", now()))
    return {"ok": True}


@app.get("/api/decks/{deck_id}/combos")
async def combos(deck_id: int):
    deck, rows = _deck_row(deck_id)
    return await advisor.find_combos(deck.get("commander") or "", [r["name"] for r in rows if r["section"] != "maybe"])


@app.get("/api/decks/{deck_id}/shopping")
async def shopping(deck_id: int):
    deck, cards = await _full_deck(deck_id)
    missing = [c for c in cards if not c["owned"] and c["section"] != "maybe"]
    borrowed = [c for c in cards if c["owned"] and c["in_decks"] and c["owned_qty"] <= len(c["in_decks"])]
    total = round(sum((c.get("eur") or 0) * c["qty"] for c in missing), 2)
    return {
        "missing": [{"name": c["name"], "eur": c.get("eur"), "cardmarket": c.get("cardmarket"), "qty": c["qty"]} for c in missing],
        "borrowed": [{"name": c["name"], "in_decks": c["in_decks"]} for c in borrowed],
        "total_eur": total,
        "budget_eur": deck.get("budget_eur"),
    }


@app.get("/api/decks/{deck_id}/export", response_class=PlainTextResponse)
def export(deck_id: int):
    deck, rows = _deck_row(deck_id)
    lines = ["Commander"] + [f"{r['qty']} {r['name']}" for r in rows if r["section"] == "commander"]
    lines += ["", "Deck"] + [f"{r['qty']} {r['name']}" for r in sorted(rows, key=lambda r: r["name"]) if r["section"] == "main"]
    maybe = [f"{r['qty']} {r['name']}" for r in rows if r["section"] == "maybe"]
    if maybe:
        lines += ["", "Maybe"] + maybe
    return "\n".join(lines)


class SuggestReq(BaseModel):
    deep: bool = False
    focus: str = ""
    count: int = 8


@app.post("/api/decks/{deck_id}/suggest")
async def suggest(deck_id: int, body: SuggestReq):
    deck, cards = await _full_deck(deck_id)
    ana = analysis.analyse(deck, cards)
    commander = deck.get("commander") or ""
    ci = set(ana["color_identity"])
    in_deck = {c["name"].lower() for c in cards}
    owned, used = ownership(exclude_deck=deck_id)

    ed = await advisor.edhrec_commander(commander) if commander else {}
    for c in cards:
        c["edhrec_inclusion"] = (ed.get(c["name"]) or {}).get("inclusion")

    # Kandidaten: EDHREC-Empfehlungen + passende Karten aus der Sammlung
    pool = [n for n in ed if n.lower() not in in_deck][:150]
    coll_names = [n for n in owned if n not in in_deck]
    coll_cards = scryfall.cached_any(coll_names)
    pool += [c["name"] for c in coll_cards.values() if set(c.get("color_identity", [])) <= ci and c["name"].lower() not in in_deck]
    found, _ = await scryfall.get_cards(list(dict.fromkeys(pool)), fuzzy_fallback=False)

    allowed_gc = {1: 0, 2: 0, 3: 3}.get(deck.get("bracket") or 2, 99) - len(ana["game_changers"])
    cands = []
    for name, c in found.items():
        if not set(c.get("color_identity", [])) <= ci or not c.get("legal_commander") or c["name"].lower() in in_deck:
            continue
        if c.get("game_changer") and allowed_gc <= 0:
            continue
        if "land" in (c.get("type_line") or "").lower() and "basic" in (c.get("type_line") or "").lower():
            continue
        key = c["name"].lower()
        e = ed.get(c["name"]) or {}
        is_owned = owned.get(key, 0) >= 1
        if not is_owned and not e:
            continue
        cands.append({
            "name": c["name"], "type": c.get("type_line"), "cmc": c.get("cmc"), "text": (c.get("oracle_text") or "")[:220],
            "owned": is_owned, "in_deck": used.get(key, []), "eur": c.get("eur"),
            "synergy": e.get("synergy"), "inclusion": e.get("inclusion"), "edhrec_list": e.get("header"),
            "game_changer": c.get("game_changer"),
        })
    cands.sort(key=lambda x: (not x["owned"], -(x["synergy"] or 0)))
    cands = cands[:120]

    payload = {
        "commander": commander,
        "bracket_target": deck.get("bracket"),
        "budget_eur": deck.get("budget_eur"),
        "wunsch_anzahl_tausche": body.count,
        "fokus": body.focus or None,
        "analyse": {k: ana[k] for k in ("counts", "targets", "advice", "avg_cmc", "game_changers", "bracket_estimate")},
        "deck": [{"name": c["name"], "type": c.get("type_line"), "cmc": c.get("cmc"), "rollen": c.get("categories"),
                  "edhrec_inclusion": c.get("edhrec_inclusion"), "text": (c.get("oracle_text") or "")[:160]}
                 for c in cards if c["section"] == "main"],
        "kandidaten": cands,
    }
    if advisor.ANTHROPIC_KEY:
        try:
            result = await advisor.ask_claude(payload, body.deep)
        except Exception as e:  # noqa: BLE001 – Fehler an die Oberfläche geben, Fallback liefern
            result = advisor.fallback(cards, cands, deck.get("budget_eur") or 0, body.count)
            result["summary"] = f"KI nicht erreichbar ({e}). " + result["summary"]
    else:
        result = advisor.fallback(cards, cands, deck.get("budget_eur") or 0, body.count)

    # Fakten prüfen: raus muss im Deck sein, rein muss ein echter Kandidat sein
    by_name = {c["name"].lower(): c for c in cands}
    deck_names = {c["name"].lower() for c in cards if c["section"] == "main"}
    checked, spent = [], 0.0
    for s in result.get("swaps", []):
        cand = by_name.get((s.get("in") or "").lower())
        if not cand or (s.get("out") or "").lower() not in deck_names:
            continue
        price = 0 if cand["owned"] else (cand.get("eur") or 0)
        spent += price
        checked.append({**s, "in": cand["name"], "owned": cand["owned"], "in_deck": cand["in_deck"], "eur": cand.get("eur"),
                        "image": (found.get(cand["name"]) or {}).get("image_small")})
    return {"summary": result.get("summary"), "swaps": checked, "cost_eur": round(spent, 2), "model": result.get("model"),
            "edhrec": bool(ed), "candidates": len(cands)}


# ---------- Commander aus Sammlung ----------
@app.get("/api/commanders/owned")
def owned_commanders():
    owned, _ = ownership()
    data = scryfall.cached_any(list(owned))
    cards = list(data.values())
    out = []
    for c in cards:
        tl = c.get("type_line") or ""
        if not (("Legendary" in tl and "Creature" in tl) or "can be your commander" in (c.get("oracle_text") or "")):
            continue
        ci = set(c.get("color_identity", []))
        fits = [x for x in cards if set(x.get("color_identity", [])) <= ci and x["name"] != c["name"] and "Basic" not in (x.get("type_line") or "")]
        out.append({"name": c["name"], "color_identity": c.get("color_identity"), "image_small": c.get("image_small"),
                    "type_line": tl, "owned_fitting": len(fits)})
    return sorted(out, key=lambda x: -x["owned_fitting"])


@app.get("/api/commanders/{name}/fit")
async def commander_fit(name: str):
    """Wie viel von der EDHREC-Liste dieses Commanders besitze ich schon?"""
    ed = await advisor.edhrec_commander(name)
    owned, used = ownership()
    have = [{"name": n, **v, "in_decks": used.get(n.lower(), [])} for n, v in ed.items() if n.lower() in owned]
    return {"edhrec_cards": len(ed), "owned": len(have), "percent": round(100 * len(have) / len(ed)) if ed else 0,
            "cards": sorted(have, key=lambda x: -(x["synergy"] or 0))}


@app.get("/api/autocomplete")
async def autocomplete(q: str):
    if len(q) < 2:
        return []
    try:
        return await scryfall.autocomplete(q)
    except Exception:  # noqa: BLE001
        return []


app.mount("/static", StaticFiles(directory=STATIC), name="static")


@app.get("/")
def index():
    return FileResponse(STATIC / "index.html")
