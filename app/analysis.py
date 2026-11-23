"""Deck-Analyse: Kurve, Kategorien (Ramp/Draw/Removal/…), Legalität, Bracket-Schätzung.

Die Kategorien sind eine Heuristik über den Oracle-Text – gut genug für Zählungen,
nicht perfekt. Grenzfälle markiert die KI-Beratung.
"""
import re

TARGETS = {  # Faustregeln für Commander (Command-Zone-Template, grob)
    "lands": (35, 38),
    "ramp": (10, 14),
    "draw": (10, 14),
    "removal": (8, 12),
    "wipe": (2, 4),
    "protection": (2, 5),
}

LABELS = {
    "ramp": "Ramp",
    "draw": "Kartenvorteil",
    "removal": "Gezieltes Removal",
    "wipe": "Brettwischer",
    "protection": "Schutz",
}

BASICS = {"plains", "island", "swamp", "mountain", "forest", "wastes"}


def _t(card):
    return (card.get("oracle_text") or "").lower()


def categories(card: dict) -> list[str]:
    t, tl = _t(card), (card.get("type_line") or "").lower()
    cats = []
    if "land" in tl and "creature" not in tl:
        return ["land"]
    if (
        re.search(r"add \{[wubrgc]\}|add one mana|add .* mana of any|add \w+ mana", t)
        or re.search(r"search your library for (a|an|up to \w+) .*land", t)
        or ("treasure" in t and "create" in t)
        or "put a land card from your hand onto the battlefield" in t
        or "you may put a land" in t
    ):
        cats.append("ramp")
    if re.search(r"draw (a|two|three|x|\w+) cards?|draws? cards?|discover \d|discover x|cascade", t) or (
        "exile the top" in t and "you may (play|cast)" in t
    ):
        cats.append("draw")
    if re.search(r"(destroy|exile) (all|each) (creature|nonland|other creature|artifact|permanent)", t) or re.search(
        r"deals? \w+ damage to each creature", t
    ):
        cats.append("wipe")
    if re.search(
        r"(destroy|exile) (target|up to (one|two|three) target)|deals? (\d+|x|that much) damage to (any target|target creature|up to one target creature|target opponent or planeswalker and \d+ damage to up to one target creature)|fights? (target|another target|up to one target)|return target .* to its owner's hand|counter target",
        t,
    ):
        cats.append("removal")
    if re.search(r"(indestructible|hexproof|shroud|protection from|phase out)", t) and re.search(
        r"(creatures you control|target creature you control|permanents you control|you control gain|equipped creature)", t
    ):
        cats.append("protection")
    return cats


def color_sources(cards: list[dict]) -> dict:
    """Zählt, wie viele Länder/Manaquellen jede Farbe erzeugen können."""
    out = {c: 0 for c in "WUBRG"}
    for c in cards:
        if "land" not in (c.get("type_line") or "").lower():
            continue
        for col in c.get("produced_mana") or []:
            if col in out:
                out[col] += c.get("qty", 1)
    return out


def analyse(deck: dict, cards: list[dict]) -> dict:
    """cards: Liste von Scryfall-Karten mit Zusatzfeldern qty, section."""
    commanders = [c for c in cards if c.get("section") == "commander"]
    main = [c for c in cards if c.get("section") != "maybe"]
    ci = set()
    for c in commanders:
        ci |= set(c.get("color_identity", []))

    total = sum(c.get("qty", 1) for c in main)
    curve = {str(i): 0 for i in range(8)}
    cats = {k: [] for k in LABELS}
    types = {}
    nonland_cmc = []
    problems, gcs, notes = [], [], []

    for c in main:
        qty = c.get("qty", 1)
        tl = c.get("type_line") or ""
        main_type = next(
            (t for t in ["Land", "Creature", "Planeswalker", "Battle", "Instant", "Sorcery", "Artifact", "Enchantment"] if t in tl),
            "Sonstiges",
        )
        types[main_type] = types.get(main_type, 0) + qty
        cs = categories(c)
        c["categories"] = cs
        if "land" not in cs:
            cmc = int(c.get("cmc") or 0)
            curve[str(min(cmc, 7))] += qty
            nonland_cmc += [c.get("cmc") or 0] * qty
        for k in cs:
            if k in cats:
                cats[k].append(c["name"])
        if c.get("game_changer"):
            gcs.append(c["name"])
        if ci and not set(c.get("color_identity", [])) <= ci:
            problems.append(f"{c['name']} liegt außerhalb der Farbidentität des Commanders")
        if not c.get("legal_commander", True):
            problems.append(f"{c['name']} ist in Commander nicht legal")
        if qty > 1 and c["name"].lower() not in BASICS and "any number of cards named" not in _t(c):
            problems.append(f"{c['name']} ist {qty}x im Deck (Singleton!)")
        t = _t(c)
        if "extra turn" in t:
            notes.append(f"{c['name']}: Extrazug")
        if re.search(r"destroy all lands|each player sacrifices .* lands", t):
            notes.append(f"{c['name']}: Massen-Landzerstörung")

    lands = types.get("Land", 0)
    if total != 100:
        problems.append(f"Deck hat {total} Karten statt 100")
    if not commanders:
        problems.append("Kein Commander gesetzt")

    counts = {"lands": lands, **{k: len(v) for k, v in cats.items()}}
    advice = []
    for k, (lo, hi) in TARGETS.items():
        v = counts.get(k, 0)
        label = "Länder" if k == "lands" else LABELS[k]
        if v < lo:
            advice.append({"key": k, "level": "low", "text": f"{label}: {v} (Richtwert {lo}–{hi}) – eher zu wenig"})
        elif v > hi:
            advice.append({"key": k, "level": "high", "text": f"{label}: {v} (Richtwert {lo}–{hi}) – eher viel"})

    bracket_est, bracket_why = estimate_bracket(gcs, notes)
    avg = round(sum(nonland_cmc) / len(nonland_cmc), 2) if nonland_cmc else 0
    return {
        "total": total,
        "color_identity": sorted(ci, key="WUBRG".index),
        "types": types,
        "curve": curve,
        "avg_cmc": avg,
        "counts": counts,
        "targets": TARGETS,
        "category_cards": cats,
        "advice": advice,
        "problems": problems,
        "game_changers": gcs,
        "notes": notes,
        "bracket_estimate": bracket_est,
        "bracket_reason": bracket_why,
        "color_sources": color_sources(main),
    }


def estimate_bracket(gcs, notes) -> tuple[int, str]:
    """Grobe Schätzung nach den offiziellen Bracket-Regeln (Combos kommen extra dazu)."""
    if any("Landzerstörung" in n for n in notes) or len(gcs) > 3:
        return 4, f"{len(gcs)} Game Changer" + (" + Massen-Landzerstörung" if notes else "")
    if gcs:
        return 3, f"{len(gcs)} Game Changer (Bracket 3 erlaubt bis zu 3)"
    if any("Extrazug" in n for n in notes):
        return 3, "Extrazug-Karten vorhanden"
    return 2, "Keine Game Changer – Precon-Niveau oder leicht darüber"
