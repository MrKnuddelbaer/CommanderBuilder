"""Deck-Analyse: Kurve, Kategorien (Ramp/Draw/Removal/…), Legalität, Bracket-Schätzung.

Die Kategorien sind eine Heuristik über den Oracle-Text – gut genug für Zählungen,
nicht perfekt. Grenzfälle markiert die KI-Beratung.
"""
import re

from . import knowledge as K

LABELS = {
    "ramp": "Ramp",
    "draw": "Kartenvorteil",
    "removal": "Gezieltes Removal",
    "wipe": "Brettwischer",
    "protection": "Schutz",
    "wincon": "Wincons",
    "synergy": "Plan/Synergie",
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
    if re.search(r"creatures you control get \+\d+/\+\d+ and gain trample|win the game|each opponent loses \d+ life|double strike and trample|extra combat", t):
        cats.append("wincon")
    return cats


def card_roles(card: dict) -> list[str]:
    """Vom Spieler zugewiesene Rolle zuerst, dann die Heuristik."""
    cats = categories(card)
    role = card.get("role")
    if role and role not in cats:
        cats = [role] + [c for c in cats if c != "land"]
    elif role:
        cats = [role] + [c for c in cats if c != role]
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


def analyse(deck: dict, cards: list[dict], gc_set=None, archetype=None) -> dict:
    """cards: Scryfall-Karten mit Zusatzfeldern qty, section, role."""
    gc_set = gc_set or K.GAME_CHANGERS
    commanders = [c for c in cards if c.get("section") == "commander"]
    main = [c for c in cards if c.get("section") != "maybe"]
    ci = set()
    for c in commanders:
        ci |= set(c.get("color_identity", []))
    cmd_mv = max([c.get("cmc") or 0 for c in commanders] or [0])
    targets = K.adjusted_targets(cmd_mv, archetype or deck.get("archetype"), len(ci))

    total = sum(c.get("qty", 1) for c in main)
    curve = {str(i): 0 for i in range(8)}
    cats = {k: [] for k in LABELS}
    types = {}
    nonland_cmc = []
    problems, gcs, notes, nogos, salty = [], [], [], [], []

    for c in main:
        qty = c.get("qty", 1)
        tl = c.get("type_line") or ""
        main_type = next(
            (t for t in ["Land", "Creature", "Planeswalker", "Battle", "Instant", "Sorcery", "Artifact", "Enchantment"] if t in tl),
            "Sonstiges",
        )
        types[main_type] = types.get(main_type, 0) + qty
        cs = card_roles(c)
        c["categories"] = cs
        if "land" not in cs:
            cmc = int(c.get("cmc") or 0)
            curve[str(min(cmc, 7))] += qty
            nonland_cmc += [c.get("cmc") or 0] * qty
        for k in cs:
            if k in cats and c.get("section") != "commander":
                cats[k].append(c["name"])
        is_gc = c.get("game_changer") or c["name"] in gc_set
        c["game_changer"] = bool(is_gc)
        if is_gc:
            gcs.append(c["name"])
        if c["name"] in K.SALT_TOP:
            salty.append({"name": c["name"], "salt": K.SALT_TOP[c["name"]]})
        for f in K.nogo_flags(c):
            nogos.append({"name": c["name"], "flag": f, "label": K.NOGO_LABELS[f]})
        if ci and not set(c.get("color_identity", [])) <= ci:
            problems.append(f"{c['name']} liegt außerhalb der Farbidentität des Commanders")
        if not c.get("legal_commander", True):
            problems.append(f"{c['name']} ist in Commander nicht legal")
        if qty > 1 and c["name"].lower() not in BASICS and "any number of cards named" not in _t(c):
            problems.append(f"{c['name']} ist {qty}x im Deck (Singleton!)")
        t = _t(c)
        if "extra turn" in t:
            notes.append(f"{c['name']}: Extrazug")
        if any(n["flag"] == "mld" and n["name"] == c["name"] for n in nogos):
            notes.append(f"{c['name']}: Massen-Landzerstörung")

    lands = types.get("Land", 0)
    if total != 100:
        problems.append(f"Deck hat {total} Karten statt 100")
    if not commanders:
        problems.append("Kein Commander gesetzt")

    counts = {"lands": lands, **{k: len(v) for k, v in cats.items()}}
    advice = []
    for k, (crit, lo, hi, top) in targets.items():
        v = counts.get(k, 0)
        label = "Länder" if k == "lands" else LABELS.get(k, k)
        if v < crit:
            advice.append({"key": k, "level": "critical", "text": f"{label}: {v} – deutlich zu wenig (Ziel {lo}–{hi})"})
        elif v < lo:
            advice.append({"key": k, "level": "low", "text": f"{label}: {v} – eher zu wenig (Ziel {lo}–{hi})"})
        elif v > top:
            advice.append({"key": k, "level": "high", "text": f"{label}: {v} – eher viel (Ziel {lo}–{hi})"})

    avg = round(sum(nonland_cmc) / len(nonland_cmc), 2) if nonland_cmc else 0
    big = sum(1 for x in nonland_cmc if x >= 7)
    if avg > 3.5:
        advice.append({"key": "curve", "level": "low", "text": f"Ø-Manawert {avg} ist hoch (Ziel ~3). Kürze von oben: teure, langsame Karten zuerst."})
    if big > 4:
        advice.append({"key": "curve", "level": "low", "text": f"{big} Karten mit Manawert 7+. Statistisch wirkst du pro Spiel nur 1–2 davon."})
    tapped = [c["name"] for c in main if "Land" in (c.get("type_line") or "") and "enters tapped" in _t(c) and "unless" not in _t(c)]
    if len(tapped) > 4:
        advice.append({"key": "lands", "level": "low", "text": f"{len(tapped)} Länder kommen immer getappt ins Spiel (Ziel ≤ 4)."})

    bracket_est, bracket_why = estimate_bracket(gcs, notes)
    return {
        "total": total,
        "color_identity": sorted(ci, key="WUBRG".index),
        "commander_mv": cmd_mv,
        "types": types,
        "curve": curve,
        "avg_cmc": avg,
        "counts": counts,
        "targets": {k: [v[1], v[2]] for k, v in targets.items()},
        "targets_full": targets,
        "category_cards": cats,
        "advice": advice,
        "problems": problems,
        "game_changers": gcs,
        "notes": notes,
        "nogos": nogos,
        "salty": salty,
        "bracket_estimate": bracket_est,
        "bracket_reason": bracket_why,
        "color_sources": color_sources(main),
        "tapped_lands": tapped,
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
