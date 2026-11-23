"""Deckbau-Coach: Profil, Deck-Finder, geführter Assistent, Karten-Feedback, Combo-/Bracket-Check, Coach-Chat.

Prinzip „Lehrer-Modus“: Der Coach erklärt, zeigt Optionen mit Begründung und fragt zurück.
Entscheiden tut immer Fabian. Combos werden aktiv gezeigt, aber nie automatisch eingebaut.
"""
import json
import re

import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from . import advisor, analysis, knowledge as K, scryfall
from .core import _deck_row, _full_deck, _resolve_list, _save_cards, ownership
from .db import db, meta_get, meta_set, now

router = APIRouter(prefix="/api")


# ---------------------------------------------------------------- Profil & Wissen
def get_profile() -> dict:
    p, _ = meta_get("profile", None)
    return {**K.DEFAULT_PROFILE, **(p or {})}


@router.get("/profile")
def profile():
    return get_profile()


@router.put("/profile")
def save_profile(body: dict):
    p = {**get_profile(), **{k: v for k, v in body.items() if k in K.DEFAULT_PROFILE}}
    meta_set("profile", p)
    return p


@router.get("/knowledge")
def knowledge():
    return {
        "glossary": K.GLOSSARY,
        "archetypes": K.ARCHETYPES,
        "brackets": K.BRACKETS,
        "steps": K.STEPS,
        "questionnaire": K.QUESTIONNAIRE,
        "roles": K.ROLE_LABELS,
        "nogo_labels": K.NOGO_LABELS,
    }


# ---------------------------------------------------------------- Deck-Finder
class Answers(BaseModel):
    answers: dict


@router.post("/finder/questionnaire")
async def finder_questionnaire(body: Answers):
    prof = get_profile()
    prof["questionnaire"] = body.answers
    meta_set("profile", prof)
    top = K.score_questionnaire(body.answers)
    # Passende Commander aus der Sammlung: Beispiel-Commander, die er besitzt, plus Farbabgleich
    owned, _ = ownership()
    owned_cards = scryfall.cached_any(list(owned))
    legends = [c for c in owned_cards.values() if "Legendary" in (c.get("type_line") or "") and "Creature" in (c.get("type_line") or "")]
    for a in top:
        a["owned_examples"] = [e for e in a["examples"] if e.lower() in owned]
        a["avoid"] = a["id"] == "combo" and "combos_early" in prof.get("nogos", [])
    return {"top": top, "owned_legends": len(legends)}


@router.get("/finder/commander")
async def finder_commander(name: str):
    """Einstieg über einen Commander: was kann er, welche Themen, wie viel besitze ich schon?"""
    found, nf = await scryfall.get_cards([name])
    if not found:
        raise HTTPException(404, f"Commander nicht gefunden: {name}")
    c = list(found.values())[0]
    page = await advisor.edhrec_page(c["name"])
    owned, used = ownership()
    have = [n for n in page["cards"] if n.lower() in owned]
    gcs = await scryfall.game_changers()
    return {
        "card": c,
        "is_game_changer": c["name"] in gcs,
        "themes": page["themes"],
        "edhrec_cards": len(page["cards"]),
        "owned_from_edhrec": len(have),
        "owned_examples": have[:15],
        "percent": round(100 * len(have) / len(page["cards"])) if page["cards"] else 0,
        "edhrec_url": f"https://edhrec.com/commanders/{advisor.edhrec_slug(c['name'])}",
    }


# ---------------------------------------------------------------- Assistent
class WizardStart(BaseModel):
    name: str
    commander: str
    bracket: int = 2
    budget_eur: float = 25
    archetype: str | None = None
    plan: str = ""
    table_notes: str = ""


@router.post("/wizard/start")
async def wizard_start(body: WizardStart):
    resolved, nf = await _resolve_list([{"name": body.commander, "qty": 1, "section": "commander", "role": None}])
    if not resolved:
        raise HTTPException(404, f"Commander nicht gefunden: {body.commander}")
    with db() as con:
        cur = con.execute(
            "INSERT INTO decks(name, commander, bracket, budget_eur, created_at, plan, archetype, wizard_step, mode, table_notes) "
            "VALUES (?,?,?,?,?,?,?,?,?,?)",
            (body.name, resolved[0]["name"], body.bracket, body.budget_eur, now(), body.plan, body.archetype, "plan", "wizard", body.table_notes),
        )
        _save_cards(con, cur.lastrowid, resolved)
    return {"id": cur.lastrowid}


class DeckMeta(BaseModel):
    plan: str | None = None
    archetype: str | None = None
    wizard_step: str | None = None
    mode: str | None = None
    table_notes: str | None = None


@router.patch("/decks/{deck_id}/meta")
def deck_meta(deck_id: int, body: DeckMeta):
    fields = {k: v for k, v in body.model_dump().items() if v is not None}
    if fields:
        with db() as con:
            con.execute(f"UPDATE decks SET {', '.join(k + '=?' for k in fields)} WHERE id=?", (*fields.values(), deck_id))
    return {"ok": True}


async def _context(deck_id):
    deck, cards = await _full_deck(deck_id)
    gcs = await scryfall.game_changers()
    ana = analysis.analyse(deck, cards, gc_set=gcs)
    return deck, cards, ana, gcs


def _bracket_issues(card: dict, bracket: int, gcs: set, current_gc: int) -> list[str]:
    out = []
    if card["name"] in gcs or card.get("game_changer"):
        allowed = K.BRACKETS.get(bracket, {}).get("gc", 99)
        if allowed == 0:
            out.append(f"Game Changer – in Bracket {bracket} nicht erlaubt")
        elif current_gc >= allowed:
            out.append(f"Game Changer – du hast schon {current_gc} von max. {allowed}")
        else:
            out.append(f"Game Changer – zählt gegen dein Limit ({current_gc}/{allowed})")
    flags = K.nogo_flags(card)
    if "mld" in flags and bracket <= 3:
        out.append("Massen-Landzerstörung – erst ab Bracket 4")
    return out


async def _candidates(deck, cards, ana, role, gcs, limit=40):
    ci = "".join(ana["color_identity"]) or "C"
    in_deck = {c["name"].lower() for c in cards}
    owned, used = ownership(exclude_deck=deck["id"])
    page = await advisor.edhrec_page(deck.get("commander") or "") if deck.get("commander") else {"cards": {}}
    ed = page["cards"]

    names = []
    headers = K.EDHREC_HEADERS.get(role, [])
    names += [n for n, v in ed.items() if v.get("header") in headers]
    q = K.ROLE_QUERIES.get(role)
    if q is not None:
        query = f"{q} id<={ci} f:commander".strip()
        names += [c["name"] for c in await scryfall.search(query, limit=50)]
    # eigene Karten, die die Heuristik in diese Rolle steckt
    coll = scryfall.cached_any(list(owned))
    for c in coll.values():
        if set(c.get("color_identity", [])) <= set(ana["color_identity"]) and (role in analysis.categories(c) or (role == "synergy" and c["name"] in ed)):
            names.append(c["name"])
    names = [n for n in dict.fromkeys(names) if n.lower() not in in_deck]
    found, _ = await scryfall.get_cards(names[:150], fuzzy_fallback=False)

    gc_count = len(ana["game_changers"])
    out = []
    for c in found.values():
        if not set(c.get("color_identity", [])) <= set(ana["color_identity"]) or not c.get("legal_commander", True):
            continue
        if "Basic" in (c.get("type_line") or ""):
            continue
        key = c["name"].lower()
        e = ed.get(c["name"]) or {}
        issues = _bracket_issues(c, deck.get("bracket") or 2, gcs, gc_count)
        out.append({
            "name": c["name"], "type_line": c.get("type_line"), "mana_cost": c.get("mana_cost"), "cmc": c.get("cmc"),
            "text": c.get("oracle_text"), "image": c.get("image"), "image_small": c.get("image_small"),
            "owned": owned.get(key, 0) >= 1, "in_decks": used.get(key, []), "eur": c.get("eur"), "cardmarket": c.get("cardmarket"),
            "synergy": e.get("synergy"), "inclusion": e.get("inclusion"), "edhrec_rank": c.get("edhrec_rank"),
            "roles": analysis.categories(c), "issues": issues, "nogos": [K.NOGO_LABELS[f] for f in K.nogo_flags(c)],
            "salt": K.SALT_TOP.get(c["name"]),
        })
    out.sort(key=lambda x: (bool(x["issues"] and "nicht erlaubt" in " ".join(x["issues"])), not x["owned"],
                            -(x["synergy"] or 0), x["edhrec_rank"] or 99999))
    return out[:limit]


@router.get("/decks/{deck_id}/step/{step_id}")
async def wizard_step(deck_id: int, step_id: str):
    step = next((s for s in K.STEPS if s["id"] == step_id), None)
    if not step:
        raise HTTPException(404, "Schritt unbekannt")
    deck, cards, ana, gcs = await _context(deck_id)
    role = step["role"]
    t = ana["targets_full"].get(role) if role else None
    in_role = [c for c in cards if role and role in c.get("categories", []) and c["section"] == "main"] if role else []
    cands = await _candidates(deck, cards, ana, role, gcs) if role else []
    result = {
        "step": step, "index": K.STEP_IDS.index(step_id), "total_steps": len(K.STEPS),
        "deck": deck, "analysis": {k: ana[k] for k in ("counts", "targets", "avg_cmc", "curve", "color_identity", "advice",
                                                       "game_changers", "nogos", "salty", "bracket_estimate", "bracket_reason",
                                                       "total", "commander_mv", "color_sources", "tapped_lands")},
        "target": {"critical": t[0], "from": t[1], "to": t[2], "max": t[3]} if t else None,
        "current": [{"name": c["name"], "cmc": c.get("cmc"), "note": c.get("note"), "image": c.get("image"),
                     "owned": c.get("owned"), "role": c.get("role")} for c in in_role],
        "candidates": cands,
    }
    if step_id == "commander":
        cmd = next((c for c in cards if c["section"] == "commander"), None)
        if cmd:
            page = await advisor.edhrec_page(cmd["name"])
            result["commander"] = {"card": cmd, "themes": page["themes"], "is_game_changer": cmd["name"] in gcs}
    if step_id == "lands":
        colors = len(ana["color_identity"])
        result["formula"] = {
            "burgess": round(31 + colors + (ana["commander_mv"] or 0)),
            "text": f"31 + {colors} Farben + Commander-MV {ana['commander_mv']:g} = {round(31 + colors + (ana['commander_mv'] or 0))} Länder (Rocks zählen teilweise mit: 2–3 Rocks ≈ 1 Land).",
        }
    if step_id in ("wincon", "check"):
        result["combos"] = await advisor.find_combos(deck.get("commander") or "", [c["name"] for c in cards if c["section"] != "maybe"])
    if step_id == "rule0":
        result["rule0"] = await rule0(deck_id)
    return result


class Pick(BaseModel):
    name: str
    role: str | None = None
    note: str | None = None
    section: str = "main"


@router.post("/decks/{deck_id}/pick")
async def pick(deck_id: int, body: Pick):
    """Karte mit Rolle (und optional Begründung) ins Deck – plus sofortiges Lehrer-Feedback."""
    resolved, _ = await _resolve_list([{"name": body.name, "qty": 1, "section": body.section, "role": body.role, "note": body.note}])
    if not resolved:
        raise HTTPException(404, f"Karte nicht gefunden: {body.name}")
    deck, cards, ana, gcs = await _context(deck_id)
    card = (await scryfall.get_cards([resolved[0]["name"]]))[0].get(resolved[0]["name"], {})
    feedback = card_feedback(card, body.role, deck, cards, ana, gcs)
    with db() as con:
        _save_cards(con, deck_id, resolved)
        con.execute("INSERT INTO history(deck_id, action, created_at) VALUES (?,?,?)",
                    (deck_id, f"+ {resolved[0]['name']}" + (f" ({K.ROLE_LABELS.get(body.role, body.role)})" if body.role else ""), now()))
    return {"ok": True, "name": resolved[0]["name"], "feedback": feedback}


def card_feedback(card, role, deck, cards, ana, gcs) -> list[dict]:
    """Regelbasiertes Sofort-Feedback (kostet nichts, erklärt das Warum)."""
    fb = []
    if not card:
        return fb
    heur = analysis.categories(card)
    if role and role not in heur and role not in ("synergy", "wincon"):
        fb.append({"level": "info", "text": f"Ich erkenne {card['name']} eher als {', '.join(K.ROLE_LABELS.get(h, h) for h in heur) or 'Themenkarte'} – passt die Rolle „{K.ROLE_LABELS.get(role, role)}“ wirklich?"})
    elif role:
        fb.append({"level": "good", "text": f"Passt: {card['name']} erfüllt die Rolle „{K.ROLE_LABELS.get(role, role)}“."})
    multi = [h for h in heur if h != role and h != "land"]
    if multi:
        fb.append({"level": "good", "text": f"Bonus: zählt zusätzlich als {', '.join(K.ROLE_LABELS.get(h, h) for h in multi)} – Doppelrollen sind Gold wert."})
    for issue in _bracket_issues(card, deck.get("bracket") or 2, gcs, len(ana["game_changers"])):
        fb.append({"level": "warn", "text": issue})
    prof = get_profile()
    for f in K.nogo_flags(card):
        lvl = "warn" if f in prof.get("nogos", []) else "info"
        fb.append({"level": lvl, "text": f"Achtung {K.NOGO_LABELS[f]}: Das steht auf deiner No-Go-Liste." if lvl == "warn" else f"Hinweis: {K.NOGO_LABELS[f]}"})
    if (card.get("cmc") or 0) >= 7:
        fb.append({"level": "info", "text": f"Manawert {card.get('cmc'):g}: Pro Spiel wirkst du im Schnitt nur 1–2 Karten mit 7+. Lohnt sich die hier besonders?"})
    if card["name"] in K.SALT_TOP:
        fb.append({"level": "warn", "text": f"Salt {K.SALT_TOP[card['name']]}: eine der unbeliebtesten Karten – vorher am Tisch ansagen."})
    if "power" in card and card.get("toughness") and (deck.get("commander") or "").startswith("Pantlaza") and "Dinosaur" in (card.get("type_line") or ""):
        try:
            fb.append({"level": "good", "text": f"Dino mit Widerstandskraft {card['toughness']} → Pantlaza löst Discover {int(card['toughness'])} aus."})
        except ValueError:
            pass
    return fb


class RoleSet(BaseModel):
    name: str
    role: str | None = None
    note: str | None = None


@router.post("/decks/{deck_id}/role")
def set_role(deck_id: int, body: RoleSet):
    with db() as con:
        con.execute("UPDATE deck_cards SET role=?, note=COALESCE(?, note) WHERE deck_id=? AND name=?", (body.role, body.note, deck_id, body.name))
    return {"ok": True}


# ---------------------------------------------------------------- Check & Rule 0
@router.get("/decks/{deck_id}/check")
async def full_check(deck_id: int):
    deck, cards, ana, gcs = await _context(deck_id)
    combos = await advisor.find_combos(deck.get("commander") or "", [c["name"] for c in cards if c["section"] != "maybe"])
    b = deck.get("bracket") or 2
    rules = K.BRACKETS[b]
    findings = []
    gc = ana["game_changers"]
    if len(gc) > rules["gc"]:
        findings.append({"level": "critical", "text": f"{len(gc)} Game Changer, Bracket {b} erlaubt {rules['gc'] if rules['gc'] < 99 else 'beliebig viele'}: {', '.join(gc)}"})
    cmd = next((c for c in cards if c["section"] == "commander"), None)
    if cmd and cmd["name"] in gcs and b <= 2:
        findings.append({"level": "critical", "text": f"Dein Commander {cmd['name']} ist ein Game Changer – erst ab Bracket 3."})
    two_card = [x for x in combos.get("included", []) if len(x["cards"]) <= 2]
    if combos.get("included"):
        if b <= 2:
            findings.append({"level": "critical", "text": f"{len(combos['included'])} Combo(s) im Deck – in Bracket {b} nicht vorgesehen. Teile entfernen oder höheres Bracket ansagen."})
        elif b == 3:
            for x in combos["included"]:
                if x["bracket_tag"] == "R" or len(x["cards"]) <= 2:
                    findings.append({"level": "warn", "text": f"Combo {' + '.join(x['cards'])} ({x['bracket_label']}) könnte vor Zug 6 zünden – in Bracket 3 ansagen oder entschärfen."})
    mld = [n["name"] for n in ana["nogos"] if n["flag"] == "mld"]
    if mld and b <= 3:
        findings.append({"level": "critical", "text": f"Massen-Landzerstörung ({', '.join(mld)}) – erst ab Bracket 4."})
    extra = [n for n in ana["notes"] if "Extrazug" in n]
    if len(extra) >= 2 and b <= 3:
        findings.append({"level": "warn", "text": "Mehrere Extrazug-Karten – Chaining ist in Bracket 1–3 tabu."})
    prof = get_profile()
    for n in ana["nogos"]:
        if n["flag"] in prof.get("nogos", []):
            findings.append({"level": "warn", "text": f"{n['name']}: {n['label']} – steht auf deiner No-Go-Liste."})
    for s in ana["salty"]:
        findings.append({"level": "info", "text": f"{s['name']} (Salt {s['salt']}) – vorher ansagen."})
    for a in ana["advice"]:
        findings.append({"level": "critical" if a["level"] == "critical" else "warn" if a["level"] == "low" else "info", "text": a["text"]})
    for p in ana["problems"]:
        findings.append({"level": "critical", "text": p})
    est = ana["bracket_estimate"]
    if combos.get("included"):
        est = max(est, 4 if (two_card and any(x["bracket_tag"] == "R" for x in two_card)) else 3)
    if mld:
        est = max(est, 4)
    return {"bracket_target": b, "bracket_rules": rules, "bracket_estimate": est, "bracket_reason": ana["bracket_reason"],
            "combos": combos, "findings": findings, "analysis": ana}


@router.get("/decks/{deck_id}/rule0")
async def rule0(deck_id: int):
    chk = await full_check(deck_id)
    deck, _ = _deck_row(deck_id)
    combos = chk["combos"].get("included", [])
    lines = [
        f"Deck: {deck['name']} – Commander: {deck.get('commander')}",
        f"Bracket: {chk['bracket_target']} ({K.BRACKETS[chk['bracket_target']]['name']}), eigene Einschätzung: {chk['bracket_estimate']}",
        f"Plan: {deck.get('plan') or '(noch kein Satz – im Assistenten Schritt „Spielplan“ eintragen)'}",
        f"Game Changer: {', '.join(chk['analysis']['game_changers']) or 'keine'}",
        f"Combos: {'; '.join(' + '.join(c['cards']) for c in combos) or 'keine bekannten'}",
    ]
    salty = [s["name"] for s in chk["analysis"]["salty"]]
    if salty:
        lines.append(f"Ansagen: {', '.join(salty)}")
    lines.append("Frage an den Tisch: „Passt das für euch? Gibt es etwas, das ihr heute nicht sehen wollt?“")
    return {"text": "\n".join(lines)}


# ---------------------------------------------------------------- Coach-Chat (Claude)
COACH_SYSTEM = """Du bist Fabians persönlicher Commander-Deckbau-Coach (Magic: The Gathering) und sprichst Deutsch.
Dein Stil ist der eines geduldigen Lehrers:
- Fabian lernt Deckbau von Grund auf. Erkläre Fachbegriffe kurz in Klammern, wenn sie zum ersten Mal auftauchen.
- Du triffst KEINE Entscheidungen für ihn. Zeige 2–3 Optionen mit Vor- und Nachteilen und konkreten Kartenbeispielen, dann frag, was er bevorzugt und warum.
- Stelle am Ende eine Rückfrage, die ihn selbst nachdenken lässt (z. B. „Welche dieser Karten würdest du zuerst streichen?“).
- Er mag große Momente, clevere Kombis und Chaos/Zufall. Er mag KEINE langen Züge, Stax/Lock und Massen-Landzerstörung.
- Infinite-Combos darfst du aktiv vorschlagen, erkläre dann Schritt für Schritt, wie sie funktionieren, und sag, ab welchem Bracket sie passen.
- Respektiere Ziel-Bracket und Budget aus dem Kontext. Erfinde keine Kartentexte: Nutze die Kartendaten aus dem Kontext; bei Karten ohne Daten sag, dass er sie prüfen soll.
- Antworte knapp und handyfreundlich (max. ~180 Wörter), Listen statt langer Absätze."""


class CoachMsg(BaseModel):
    message: str
    step: str | None = None
    history: list[dict] = []


@router.post("/decks/{deck_id}/coach")
async def coach_chat(deck_id: int, body: CoachMsg):
    if not advisor.ANTHROPIC_KEY:
        raise HTTPException(400, "Für den Coach-Chat fehlt ANTHROPIC_API_KEY in Railway.")
    deck, cards, ana, gcs = await _context(deck_id)
    step = next((s for s in K.STEPS if s["id"] == body.step), None)
    ctx = {
        "deck": {k: deck.get(k) for k in ("name", "commander", "bracket", "budget_eur", "plan", "archetype", "table_notes")},
        "bracket_regeln": K.BRACKETS.get(deck.get("bracket") or 2),
        "aktueller_schritt": step and {"titel": step["title"], "lektion": step["lesson"]},
        "analyse": {k: ana[k] for k in ("counts", "targets", "avg_cmc", "advice", "game_changers", "nogos")},
        "karten": [{"name": c["name"], "rolle": c.get("role") or (c.get("categories") or [None])[0], "mv": c.get("cmc"),
                    "typ": c.get("type_line"), "text": (c.get("oracle_text") or "")[:200]} for c in cards if c["section"] != "maybe"][:100],
        "profil": get_profile(),
    }
    messages = [{"role": "user", "content": "Kontext (JSON):\n" + json.dumps(ctx, ensure_ascii=False)},
                {"role": "assistant", "content": "Verstanden. Ich coache Fabian im Lehrer-Stil."}]
    for h in body.history[-8:]:
        if h.get("role") in ("user", "assistant") and h.get("content"):
            messages.append({"role": h["role"], "content": str(h["content"])[:2000]})
    messages.append({"role": "user", "content": body.message})
    async with httpx.AsyncClient(timeout=120) as c:
        r = await c.post("https://api.anthropic.com/v1/messages",
                         headers={"x-api-key": advisor.ANTHROPIC_KEY, "anthropic-version": "2023-06-01", "content-type": "application/json"},
                         json={"model": advisor.MODEL_DEFAULT, "max_tokens": 1200, "system": COACH_SYSTEM, "messages": messages})
        if r.status_code != 200:
            raise HTTPException(502, f"Claude-API: {r.text[:200]}")
        text = "".join(b.get("text", "") for b in r.json().get("content", []))
    return {"reply": text}
