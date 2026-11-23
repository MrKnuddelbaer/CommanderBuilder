"""Scryfall-Anbindung mit SQLite-Cache.

Scryfall bittet um max. ~10 Anfragen/Sekunde und einen eigenen User-Agent.
Karten werden 3 Tage gecacht (Preise ändern sich täglich).
"""
import asyncio
import os
import json
import time

import httpx

from .db import db

API = os.environ.get("SCRYFALL_API", "https://api.scryfall.com")
HEADERS = {"User-Agent": "CommanderBuilder/0.1 (private deckbuilding tool)", "Accept": "application/json"}
CACHE_SECONDS = 3 * 24 * 3600


def slim(card: dict) -> dict:
    """Nur die Felder behalten, die das Tool braucht."""
    faces = card.get("card_faces") or []
    oracle = card.get("oracle_text") or "\n//\n".join(f.get("oracle_text", "") for f in faces)
    image = (card.get("image_uris") or (faces[0].get("image_uris") if faces else None) or {})
    prices = card.get("prices") or {}
    return {
        "name": card["name"],
        "mana_cost": card.get("mana_cost") or (faces[0].get("mana_cost") if faces else ""),
        "cmc": card.get("cmc", 0) or 0,
        "type_line": card.get("type_line", ""),
        "oracle_text": oracle,
        "colors": card.get("colors") or (faces[0].get("colors") if faces else []) or [],
        "color_identity": card.get("color_identity", []),
        "power": card.get("power") or (faces[0].get("power") if faces else None),
        "toughness": card.get("toughness") or (faces[0].get("toughness") if faces else None),
        "legal_commander": (card.get("legalities") or {}).get("commander") == "legal",
        "game_changer": bool(card.get("game_changer")),
        "produced_mana": card.get("produced_mana", []),
        "keywords": card.get("keywords", []),
        "eur": _f(prices.get("eur")) or _f(prices.get("eur_foil")),
        "usd": _f(prices.get("usd")) or _f(prices.get("usd_foil")),
        "cardmarket": (card.get("purchase_uris") or {}).get("cardmarket"),
        "image": image.get("normal") or image.get("small"),
        "image_small": image.get("small"),
        "scryfall_uri": card.get("scryfall_uri"),
        "edhrec_rank": card.get("edhrec_rank"),
    }


def _f(v):
    try:
        return float(v) if v is not None else None
    except (TypeError, ValueError):
        return None


def _key(name: str) -> str:
    return name.strip().lower()


def _store(con, card: dict, extra_aliases=()):
    s = slim(card)
    key = _key(s["name"])
    con.execute(
        "INSERT OR REPLACE INTO cards(key, name, data, fetched_at) VALUES (?,?,?,?)",
        (key, s["name"], json.dumps(s), time.time()),
    )
    aliases = {key}
    if " // " in s["name"]:
        aliases.add(_key(s["name"].split(" // ")[0]))
    for a in extra_aliases:
        aliases.add(_key(a))
    # Universes-Beyond-Zweitnamen (z. B. FF-Namen) als Alias merken
    if card.get("flavor_name"):
        aliases.add(_key(card["flavor_name"]))
    for a in aliases:
        con.execute("INSERT OR REPLACE INTO aliases(alias, key) VALUES (?,?)", (a, key))
    return s


def cached(names) -> dict:
    """Liefert {eingegebener Name -> Karte} für alles, was frisch im Cache liegt."""
    out = {}
    with db() as con:
        for n in names:
            row = con.execute(
                "SELECT c.data, c.fetched_at FROM aliases a JOIN cards c ON c.key=a.key WHERE a.alias=?",
                (_key(n),),
            ).fetchone()
            if row and time.time() - row["fetched_at"] < CACHE_SECONDS:
                out[n] = json.loads(row["data"])
    return out


def cached_any(names) -> dict:
    """Wie cached(), ignoriert aber das Alter (für Offline-Fallback)."""
    out = {}
    with db() as con:
        for n in names:
            row = con.execute(
                "SELECT c.data FROM aliases a JOIN cards c ON c.key=a.key WHERE a.alias=?", (_key(n),)
            ).fetchone()
            if row:
                out[n] = json.loads(row["data"])
    return out


async def get_cards(names, fuzzy_fallback=True) -> tuple[dict, list]:
    """Holt Karten (Cache zuerst, dann Scryfall in 75er-Paketen).

    Rückgabe: ({eingegebener Name -> Karte}, [nicht gefundene Namen])
    """
    names = list(dict.fromkeys(n for n in names if n and n.strip()))
    found = cached(names)
    missing = [n for n in names if n not in found]
    not_found = []
    if missing:
        async with httpx.AsyncClient(headers=HEADERS, timeout=30) as client:
            for i in range(0, len(missing), 75):
                batch = missing[i : i + 75]
                try:
                    r = await client.post(
                        f"{API}/cards/collection",
                        json={"identifiers": [{"name": n} for n in batch]},
                    )
                    r.raise_for_status()
                    payload = r.json()
                except httpx.HTTPError:
                    # Scryfall nicht erreichbar: alter Cache ist besser als nichts
                    found.update(cached_any(batch))
                    not_found.extend(n for n in batch if n not in found)
                    continue
                with db() as con:
                    by_key = {}
                    for card in payload.get("data", []):
                        s = _store(con, card)
                        by_key[_key(s["name"])] = s
                        if " // " in s["name"]:
                            by_key[_key(s["name"].split(" // ")[0])] = s
                    for n in batch:
                        if _key(n) in by_key:
                            found[n] = by_key[_key(n)]
                not_found.extend(n for n in batch if n not in found)
                await asyncio.sleep(0.12)

            if fuzzy_fallback and not_found:
                still = []
                for n in not_found[:60]:
                    try:
                        r = await client.get(f"{API}/cards/named", params={"fuzzy": n})
                        if r.status_code == 200:
                            with db() as con:
                                found[n] = _store(con, r.json(), extra_aliases=[n])
                        else:
                            still.append(n)
                    except httpx.HTTPError:
                        still.append(n)
                    await asyncio.sleep(0.12)
                not_found = still + not_found[60:]
    return found, not_found


async def search(query: str, limit=40) -> list[dict]:
    """Scryfall-Volltextsuche (Syntax wie auf scryfall.com)."""
    async with httpx.AsyncClient(headers=HEADERS, timeout=30) as client:
        r = await client.get(f"{API}/cards/search", params={"q": query, "order": "edhrec"})
        if r.status_code == 404:
            return []
        r.raise_for_status()
        cards = r.json().get("data", [])[:limit]
    with db() as con:
        return [_store(con, c) for c in cards]


async def autocomplete(q: str) -> list[str]:
    async with httpx.AsyncClient(headers=HEADERS, timeout=10) as client:
        r = await client.get(f"{API}/cards/autocomplete", params={"q": q})
        r.raise_for_status()
        return r.json().get("data", [])
