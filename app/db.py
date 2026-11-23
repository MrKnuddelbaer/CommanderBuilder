"""SQLite-Datenbank. Auf Railway liegt die Datei auf einem Volume (DB_PATH=/data/app.db)."""
import os
import sqlite3
import time
from contextlib import contextmanager

DB_PATH = os.environ.get("DB_PATH", os.path.join(os.path.dirname(__file__), "..", "local.db"))

SCHEMA = """
CREATE TABLE IF NOT EXISTS cards (
    key TEXT PRIMARY KEY,          -- Oracle-Name in Kleinbuchstaben
    name TEXT NOT NULL,
    data TEXT NOT NULL,            -- schlankes JSON aus Scryfall
    fetched_at REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS aliases (
    alias TEXT PRIMARY KEY,        -- z. B. 'paradise chocobo' oder Frontseite einer DFC
    key TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS collection (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    raw_name TEXT NOT NULL,
    name TEXT,                     -- aufgelöster Oracle-Name, NULL = nicht gefunden
    set_name TEXT,
    qty INTEGER NOT NULL DEFAULT 1,
    finish TEXT,
    price_usd REAL,
    imported_at REAL
);
CREATE TABLE IF NOT EXISTS decks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    commander TEXT,
    bracket INTEGER DEFAULT 2,
    budget_eur REAL DEFAULT 25,
    notes TEXT DEFAULT '',
    created_at REAL
);
CREATE TABLE IF NOT EXISTS deck_cards (
    deck_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    qty INTEGER NOT NULL DEFAULT 1,
    section TEXT NOT NULL DEFAULT 'main',   -- commander | main | maybe
    physical INTEGER NOT NULL DEFAULT 0,    -- 1 = Karte liegt physisch im Deck (z. B. aus eigenem Precon)
    PRIMARY KEY (deck_id, name, section)
);
CREATE TABLE IF NOT EXISTS meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at REAL
);
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    deck_id INTEGER NOT NULL,
    action TEXT NOT NULL,          -- z. B. 'swap: A -> B'
    created_at REAL
);
"""


def connect():
    os.makedirs(os.path.dirname(os.path.abspath(DB_PATH)), exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con


@contextmanager
def db():
    con = connect()
    try:
        yield con
        con.commit()
    finally:
        con.close()


def init():
    with db() as con:
        con.executescript(SCHEMA)
        _add_columns(con, "deck_cards", {"physical": "INTEGER NOT NULL DEFAULT 0", "role": "TEXT", "note": "TEXT"})
        _add_columns(con, "decks", {"plan": "TEXT", "archetype": "TEXT", "wizard_step": "TEXT", "mode": "TEXT DEFAULT 'free'",
                                    "table_notes": "TEXT"})


def _add_columns(con, table, cols):
    have = {r["name"] for r in con.execute(f"PRAGMA table_info({table})")}
    for name, typ in cols.items():
        if name not in have:
            con.execute(f"ALTER TABLE {table} ADD COLUMN {name} {typ}")


def meta_get(key, default=None):
    import json
    with db() as con:
        r = con.execute("SELECT value, updated_at FROM meta WHERE key=?", (key,)).fetchone()
    return (json.loads(r["value"]), r["updated_at"]) if r else (default, 0)


def meta_set(key, value):
    import json
    with db() as con:
        con.execute("INSERT OR REPLACE INTO meta(key, value, updated_at) VALUES (?,?,?)", (key, json.dumps(value), time.time()))


def now():
    return time.time()
