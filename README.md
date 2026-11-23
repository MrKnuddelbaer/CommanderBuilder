# CommanderBuilder

Privates Commander-Deckbuilding-Tool (Magic: The Gathering) – läuft als Web-App auf Railway.

**Was es kann**
- **Sammlung:** Collectr-CSV-Export importieren, Karten werden mit Scryfall abgeglichen
- **Decks:** Precon laden (z. B. Veloci-Ramp-Tor), Textlisten importieren, Karten tauschen, Export für Moxfield/Archidekt
- **Analyse:** Manakurve, Ramp/Draw/Removal/Wipes/Schutz gegen Richtwerte, Farbquellen, Legalität, Bracket-Schätzung, Combo-Check (Commander Spellbook)
- **Berater:** Tauschvorschläge aus Sammlung + EDHREC, begründet von Claude (Sonnet normal, Opus für die Tiefenanalyse), innerhalb von Budget und Ziel-Bracket
- **Einkauf:** fehlende Karten mit Cardmarket-Preis (Scryfall) und Link
- **Commander finden:** legendäre Kreaturen aus der Sammlung, Abgleich mit EDHREC

## Umgebungsvariablen (Railway)
| Variable | Zweck |
|---|---|
| `APP_PASSWORD` | Login-Passwort (leer = kein Login) |
| `SESSION_SECRET` | beliebiger langer Zufallswert für das Login-Cookie |
| `ANTHROPIC_API_KEY` | für den KI-Berater (ohne Key: regelbasiert) |
| `DB_PATH` | `/data/app.db` – auf ein Railway-Volume unter `/data` legen |
| `MODEL_DEFAULT` / `MODEL_DEEP` | optional, Standard `claude-sonnet-5-5` / `claude-opus-5-5` |

## Lokal starten
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Tests: `python -m pytest tests/` · Offline-Test mit Fake-Scryfall: `uvicorn tests.fake_scryfall:app --port 9000` und `SCRYFALL_API=http://127.0.0.1:9000`.

Datenquellen: [Scryfall](https://scryfall.com/docs/api), [EDHREC](https://edhrec.com), [Commander Spellbook](https://commanderspellbook.com).
