"""Gemeinsame Hilfsfunktionen für Decks, Besitz und Kartenauflösung."""
from fastapi import HTTPException

from . import analysis, scryfall
from .db import db


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
        cards = [dict(r) for r in con.execute("SELECT name, qty, section, physical, role, note FROM deck_cards WHERE deck_id=?", (deck_id,))]
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
            "INSERT INTO deck_cards(deck_id, name, qty, section, physical, role, note) VALUES (?,?,?,?,?,?,?) "
            "ON CONFLICT(deck_id, name, section) DO UPDATE SET qty=qty+excluded.qty, role=COALESCE(excluded.role, role), note=COALESCE(excluded.note, note)",
            (deck_id, e["name"], e["qty"], e["section"], int(physical), e.get("role"), e.get("note")),
        )


async def _full_deck(deck_id):
    deck, rows = _deck_row(deck_id)
    found, _ = await scryfall.get_cards([r["name"] for r in rows])
    owned, used = ownership(exclude_deck=deck_id)
    cards = []
    for r in rows:
        c = dict(found.get(r["name"]) or {"name": r["name"], "type_line": "?", "oracle_text": ""})
        c.update(qty=r["qty"], section=r["section"], role=r.get("role"), note=r.get("note"))
        key = c["name"].lower()
        basic = key in analysis.BASICS
        c["physical"] = bool(r.get("physical"))
        c["owned"] = basic or c["physical"] or owned.get(key, 0) >= 1
        c["owned_qty"] = owned.get(key, 0)
        c["in_decks"] = used.get(key, [])
        cards.append(c)
    return deck, cards


