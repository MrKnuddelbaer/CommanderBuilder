"""Berater: EDHREC-Daten + Combo-Check + Claude für begründete Tauschvorschläge.

Harte Fakten (Preis, Farbidentität, Legalität) kommen immer aus Scryfall.
Claude wählt nur aus und begründet. Ohne API-Key gibt es einen regelbasierten Fallback.
"""
import json
import os
import re

import httpx

ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
MODEL_DEFAULT = os.environ.get("MODEL_DEFAULT", "claude-sonnet-5-5")
MODEL_DEEP = os.environ.get("MODEL_DEEP", "claude-opus-5-5")
UA = {"User-Agent": "CommanderBuilder/0.1"}


def edhrec_slug(name: str) -> str:
    name = name.split(" // ")[0].lower()
    name = re.sub(r"[^a-z0-9\s-]", "", name.replace("'", ""))
    return re.sub(r"[\s-]+", "-", name).strip("-")


async def edhrec_page(commander: str) -> dict:
    """EDHREC-Commanderseite (inoffizielles JSON, 24 h gecacht).
    Rückgabe: {"cards": {Name: {synergy, inclusion, header}}, "themes": [{name, count}], "num_decks": n}"""
    from .db import meta_get, meta_set
    import time

    slug = edhrec_slug(commander)
    cached, ts = meta_get(f"edhrec:{slug}", None)
    if cached and time.time() - ts < 24 * 3600:
        return cached
    url = f"https://json.edhrec.com/pages/commanders/{slug}.json"
    try:
        async with httpx.AsyncClient(headers=UA, timeout=20, follow_redirects=True) as c:
            r = await c.get(url)
            if r.status_code != 200:
                return {"cards": {}, "themes": [], "num_decks": 0}
            data = r.json()
    except (httpx.HTTPError, ValueError):
        return cached or {"cards": {}, "themes": [], "num_decks": 0}
    container = (data.get("container") or {}).get("json_dict") or {}
    lists = container.get("cardlists") or []
    cards = {}
    for lst in lists:
        header = lst.get("header", "")
        for cv in lst.get("cardviews", []):
            name = cv.get("name")
            if not name:
                continue
            inc = cv.get("inclusion") or cv.get("num_decks") or 0
            pot = cv.get("potential_decks") or 0
            cards.setdefault(name, {
                "synergy": round(cv.get("synergy", 0) or 0, 2),
                "inclusion": round(100 * inc / pot) if pot else None,
                "header": header,
            })
    themes = []
    for t in ((data.get("panels") or {}).get("taglinks") or []):
        if t.get("value"):
            themes.append({"name": t.get("value"), "count": t.get("count"), "slug": t.get("slug")})
    out = {"cards": cards, "themes": themes[:15], "num_decks": data.get("num_decks_avg") or (container.get("card") or {}).get("num_decks") or 0}
    if cards:
        meta_set(f"edhrec:{slug}", out)
    return out


async def edhrec_commander(commander: str) -> dict:
    return (await edhrec_page(commander))["cards"]


async def find_combos(commander: str, names: list[str]) -> dict:
    """Commander Spellbook: welche Combos sind komplett im Deck, welche fehlen nur 1 Karte."""
    body = {
        "commanders": [{"card": commander}] if commander else [],
        "main": [{"card": n} for n in names if n != commander],
    }
    url = "https://backend.commanderspellbook.com/find-my-combos"
    try:
        async with httpx.AsyncClient(headers=UA, timeout=40) as c:
            r = await c.post(url, json=body)
            if r.status_code >= 400:
                # Fallback: Textformat, wie es die Spellbook-Website selbst schickt
                text = (f"// Commander\n1 {commander}\n// Main\n" if commander else "") + "\n".join(f"1 {n}" for n in names if n != commander)
                r = await c.post(url, content=text.encode(), headers={"Content-Type": "text/plain"})
            if r.status_code != 200:
                return {"included": [], "almost": [], "error": f"HTTP {r.status_code}"}
            payload = r.json()
            res = payload.get("results", payload)
    except (httpx.HTTPError, ValueError) as e:
        return {"included": [], "almost": [], "error": str(e)}

    deck_set = {n.lower() for n in names} | ({commander.lower()} if commander else set())
    tag_names = {"R": "Ruthless (→ Bracket 4)", "S": "Spicy (→ Bracket 3)", "P": "Powerful (→ Bracket 3)",
                 "O": "Oddball (→ Bracket 2)", "C": "Core (→ Bracket 2)", "E": "Exhibition (→ Bracket 1)", "B": "Banned"}

    def conv(combo):
        uses = [u.get("card", {}).get("name") for u in combo.get("uses", [])]
        uses = [u for u in uses if u]
        produces = [p.get("feature", {}).get("name") for p in combo.get("produces", [])]
        tag = combo.get("bracketTag")
        return {
            "cards": uses,
            "missing": [u for u in uses if u.lower() not in deck_set and u.split(" // ")[0].lower() not in deck_set],
            "result": [p for p in produces if p][:4],
            "steps": (combo.get("description") or "").strip(),
            "prerequisites": (combo.get("notablePrerequisites") or combo.get("easyPrerequisites") or "").strip(),
            "mana_needed": combo.get("manaNeeded") or "",
            "bracket_tag": tag,
            "bracket_label": tag_names.get(tag, tag),
            "popularity": combo.get("popularity"),
            "url": f"https://commanderspellbook.com/combo/{combo.get('id')}/" if combo.get("id") else None,
        }

    almost = [conv(x) for x in (res.get("almostIncluded") or [])]
    almost = [a for a in almost if len(a["missing"]) == 1]
    almost.sort(key=lambda a: -(a.get("popularity") or 0))
    return {
        "included": [conv(x) for x in (res.get("included") or [])][:20],
        "almost": almost[:20],
    }


SYSTEM = """Du bist ein erfahrener Magic-Commander-Deckbauer und berätst Fabian auf Deutsch.
Regeln:
- Schlage nur Karten aus der Kandidatenliste vor (dort stehen echte Preise und Besitz).
- Bevorzuge Karten, die er besitzt (owned=true). Steckt eine Karte schon in einem anderen Deck (in_deck), weise darauf hin.
- Die Summe der Kaufpreise (nicht besessene Karten) darf das Budget nicht überschreiten.
- Respektiere das Ziel-Bracket: keine Game Changer über dem erlaubten Maß, Infinite-Combos nur ab Bracket 4 (in 3 nur als Hinweis).
- Jeder Tausch: eine Karte raus, eine rein, kurze konkrete Begründung (Rolle im Deck, Synergie mit dem Commander).
- Achte auf die Analyse: fehlende Kategorien (Ramp, Draw, Removal, Schutz) zuerst füllen.
Antworte NUR mit JSON: {"summary": "2-3 Sätze", "swaps": [{"out": "...", "in": "...", "reason": "..."}]}"""


async def ask_claude(payload: dict, deep: bool) -> dict:
    model = MODEL_DEEP if deep else MODEL_DEFAULT
    async with httpx.AsyncClient(timeout=180) as c:
        r = await c.post(
            "https://api.anthropic.com/v1/messages",
            headers={"x-api-key": ANTHROPIC_KEY, "anthropic-version": "2023-06-01", "content-type": "application/json"},
            json={
                "model": model,
                "max_tokens": 4000,
                "system": SYSTEM,
                "messages": [{"role": "user", "content": json.dumps(payload, ensure_ascii=False)}],
            },
        )
        r.raise_for_status()
        text = "".join(b.get("text", "") for b in r.json().get("content", []))
    m = re.search(r"\{.*\}", text, re.S)
    data = json.loads(m.group(0)) if m else {"summary": text, "swaps": []}
    data["model"] = model
    return data


def fallback(deck_cards: list[dict], candidates: list[dict], budget: float, n=8) -> dict:
    """Ohne KI: beste Kandidaten (Besitz > Synergie) gegen die schwächsten Deckkarten."""
    weak = sorted(
        [c for c in deck_cards if c.get("section") == "main" and "land" not in c.get("categories", [])],
        key=lambda c: (c.get("edhrec_inclusion") or 0, -(c.get("cmc") or 0)),
    )
    candidates = [c for c in candidates if c.get("synergy") is not None]
    if not candidates:
        return {"summary": "Ohne KI und ohne EDHREC-Daten kann ich keine sinnvollen Tausche vorschlagen.", "swaps": [], "model": None}
    spent, swaps = 0.0, []
    for cand in sorted(candidates, key=lambda c: (not c["owned"], -(c.get("synergy") or 0))):
        if len(swaps) >= n or not weak:
            break
        price = 0 if cand["owned"] else (cand.get("eur") or 0)
        if spent + price > budget:
            continue
        out = weak.pop(0)
        spent += price
        swaps.append({"out": out["name"], "in": cand["name"], "reason": f"EDHREC: Synergie {cand.get('synergy'):+.0%}, in {cand.get('inclusion') or '?'} % der Decks mit diesem Commander"})
    return {"summary": "Regelbasierte Vorschläge (kein ANTHROPIC_API_KEY gesetzt).", "swaps": swaps, "model": None}
