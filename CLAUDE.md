# CommanderBuilder – Notizen für Claude

- Besitzer: Fabian (spricht Deutsch, UI und Texte auf Deutsch). Nutzt das Tool allein, Login per `APP_PASSWORD`.
- Stack: FastAPI + SQLite (`app/`), Vanilla-JS-Frontend (`static/`), Railway (Railpack, `railway.json`).
- Harte Kartendaten immer aus Scryfall (`app/scryfall.py`, Cache 3 Tage). Die KI (`app/advisor.py`) wählt nur aus Kandidaten aus; `/suggest` prüft jede Antwort gegen Deck und Kandidatenliste.
- `deck_cards.physical = 1`: Karte liegt physisch im Deck (z. B. eigenes Precon) und zählt als besessen, auch wenn sie nicht in Collectr steht.
- Brackets: 2 = Precon-Niveau (keine Game Changer), 3 = bis 3 Game Changer, 4+ = frei. Combos werden nur markiert, nie automatisch eingebaut.
- Arbeitsweise: Änderungen erst im Test-Dienst (Branch `test`), nach OK nach `main` (Live).
- Tests: `python -m pytest tests/`; Scryfall ist aus Claude-Sandboxen oft nicht erreichbar → `tests/fake_scryfall.py` nutzen.
