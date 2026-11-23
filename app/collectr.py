"""Import des Collectr-CSV-Exports.

Collectr-Namen enthalten Zusätze wie '(Showcase)', '(0334)' oder bei Universes Beyond
'Paradise Chocobo - Birds of Paradise (Borderless)'. Daraus werden Kandidaten für die
Scryfall-Suche gebaut.
"""
import csv
import io
import re

MTG = "Magic: The Gathering"
_PAREN = re.compile(r"\s*\([^()]*\)\s*$")


def candidates(raw: str) -> list[str]:
    name = raw.strip()
    while _PAREN.search(name):
        name = _PAREN.sub("", name).strip()
    out = []
    if " - " in name:
        left, right = name.split(" - ", 1)
        # Bei Zweitnamen steht der Oracle-Name meist rechts (Paradise Chocobo - Birds of Paradise)
        out += [right.strip(), left.strip(), name]
    else:
        out.append(name)
    if " // " in name:
        out.append(name.split(" // ")[0].strip())
    return list(dict.fromkeys(o for o in out if o))


def is_token(raw: str) -> bool:
    low = raw.lower()
    return "token" in low and " // " in raw


def parse(text: str) -> list[dict]:
    """Gibt nur Magic-Karten zurück, Watchlist-Einträge und Tokens werden übersprungen."""
    reader = csv.DictReader(io.StringIO(text.lstrip("﻿")))
    price_col = next((c for c in (reader.fieldnames or []) if c.startswith("Market Price")), None)
    rows = []
    for r in reader:
        if (r.get("Category") or "").strip() != MTG:
            continue
        if (r.get("Watchlist") or "").strip().lower() == "true":
            continue
        raw = (r.get("Product Name") or "").strip()
        if not raw or is_token(raw):
            continue
        try:
            qty = int(float(r.get("Quantity") or 1))
        except ValueError:
            qty = 1
        try:
            price = float(r.get(price_col) or 0) if price_col else None
        except ValueError:
            price = None
        rows.append(
            {
                "raw_name": raw,
                "candidates": candidates(raw),
                "set_name": (r.get("Set") or "").strip(),
                "qty": max(qty, 1),
                "finish": (r.get("Variance") or "").strip(),
                "price_usd": price,
            }
        )
    return rows


def parse_decklist(text: str) -> list[dict]:
    """Textliste wie '1 Sol Ring', '1x Sol Ring', 'Sol Ring' oder Abschnitte 'Commander:'."""
    out, section = [], "main"
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("//") or line.startswith("#"):
            continue
        low = line.lower().rstrip(":")
        if low in ("commander", "kommandeur"):
            section = "commander"
            continue
        if low in ("deck", "main", "mainboard", "creatures", "kreaturen", "lands", "länder"):
            section = "main"
            continue
        if low in ("maybe", "maybeboard", "sideboard", "vielleicht"):
            section = "maybe"
            continue
        m = re.match(r"^(\d+)\s*x?\s+(.+)$", line, re.I)
        qty, name = (int(m.group(1)), m.group(2)) if m else (1, line)
        name = re.sub(r"\s*\*[A-Z]+\*\s*$", "", name)                    # '*F*' entfernen
        name = re.sub(r"\s*\([A-Z0-9]{2,6}\)\s*[\w-]*\s*$", "", name).strip()  # '(LCC) 123' entfernen
        out.append({"name": name, "qty": qty, "section": section})
    return out
