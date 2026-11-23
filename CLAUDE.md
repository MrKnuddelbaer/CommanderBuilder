# CommanderBuilder – Notizen für Claude

- Besitzer: Fabian (spricht Deutsch, UI und Texte auf Deutsch). Nutzt das Tool allein, Login per `APP_PASSWORD`.
- Stack: FastAPI + SQLite (`app/`), Vanilla-JS-Frontend (`static/`), Railway (Railpack, `railway.json`).
- Harte Kartendaten immer aus Scryfall (`app/scryfall.py`, Cache 3 Tage). Die KI (`app/advisor.py`) wählt nur aus Kandidaten aus; `/suggest` prüft jede Antwort gegen Deck und Kandidatenliste.
- `deck_cards.physical = 1`: Karte liegt physisch im Deck (z. B. eigenes Precon) und zählt als besessen, auch wenn sie nicht in Collectr steht.
- Brackets: 2 = Precon-Niveau (keine Game Changer), 3 = bis 3 Game Changer, 4+ = frei. Combos werden nur markiert, nie automatisch eingebaut.
- Arbeitsweise: Änderungen erst im Test-Dienst (Branch `test`), nach OK nach `main` (Live).
- Tests: `python -m pytest tests/`; Scryfall ist aus Claude-Sandboxen oft nicht erreichbar → `tests/fake_scryfall.py` nutzen.
- Coach (v0.2, `app/coach.py`, `app/knowledge.py`, `static/coach.js`): Lehrer-Modus – erklärt, zeigt Optionen, Fabian entscheidet. Profil in `meta.profile` (No-Gos: lange Züge, Stax, MLD; Combos aktiv vorschlagen; Einsteiger-Erklärungen).
- Wissensbasis/Quellen: `docs/commander-wissen.md` (Recherche Nov. 2026). Zahlen in `knowledge.py` stammen daraus.
- Game Changer: live per Scryfall `is:gamechanger` (1x täglich in `meta`), Fallback-Liste in `knowledge.py`.
- Commander-Spellbook-Request-Format nicht verifiziert: JSON `{commanders, main}` mit Text-Fallback (`advisor.find_combos`). Bei echten Fehlern zuerst dort schauen.
