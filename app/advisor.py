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


async def edhrec_commander(commander: str) -> dict:
    """Liest die EDHREC-Commanderseite. Rückgabe: {Kartenname: {synergy, inclusion, header}}."""
    url = f"https://json.edhrec.com/pages/commanders/{edhrec_slug(commander)}.json"
    try:
        async with httpx.AsyncClient(headers=UA, timeout=20, follow_redirects=True) as c:
            r = await c.get(url)
            if r.status_code != 200:
                return {}
            data = r.json()
    except (httpx.HTTPError, ValueError):
        return {}
    lists = (((data.get("container") or {}).get("json_dict") or {}).get("cardlists")) or []
    out = {}
    for lst in lists:
        header = lst.get("header", "")
        for cv in lst.get("cardviews", []):
            name = cv.get("name")
            if not name:
                continue
            inc = cv.get("inclusion") or cv.get("num_decks") or 0
            pot = cv.get("potential_decks") or 0
            out.setdefault(
                name,
                {
                    "synergy": round(cv.get("synergy", 0) or 0, 2),
                    "inclusion": round(100 * inc / pot) if pot else None,
                    "header": header,
                },
            )
    return out


async def find_combos(commander: str, names: list[str]) -> dict:
    """Commander Spellbook: welche Combos sind komplett im Deck, welche fehlen nur 1 Karte."""
    body = {
        "commanders": [{"card": commander}] if commander else [],
        "main": [{"card": n} for n in names if n != commander],
    }
    try:
        async with httpx.AsyncClient(headers=UA, timeout=30) as c:
            r = await c.post("https://backend.commanderspellbook.com/find-my-combos", json=body)
            if r.status_code != 200:
                return {"included": [], "almost": [], "error": f"HTTP {r.status_code}"}
            res = r.json().get("results", r.json())
    except (httpx.HTTPError, ValueError) as e:
        return {"included": [], "almost": [], "error": str(e)}

    def conv(combo):
        uses = [u.get("card", {}).get("name") for u in combo.get("uses", [])]
        produces = [p.get("feature", {}).get("name") for p in combo.get("produces", [])]
        return {
            "cards": [u for u in uses if u],
            "result": [p for p in produces if p][:3],
            "bracket": combo.get("bracketTag"),
            "url": f"https://commanderspellbook.com/combo/{combo.get('id')}/" if combo.get("id") else None,
        }

    return {
        "included": [conv(x) for x in (res.get("included") or [])][:20],
        "almost": [conv(x) for x in (res.get("almostIncluded") or [])][:15],
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
