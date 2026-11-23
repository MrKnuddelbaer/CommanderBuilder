# Commander-Wissen für den Deckbau-Coach

Stand der Recherche: 23.11.2026. Kartennamen bleiben auf Englisch. Quellen stehen je Abschnitt inline als [Titel](URL).

Lesehilfe:
- **Zahl mit Quelle** = aus der Quelle übernommen.
- **"Einschätzung"** = redaktionelle Bewertung ohne harte Datenbasis (z. B. Spaßfaktor, Komplexität). In der App als Heuristik markieren, nicht als Fakt.
- Wenn Quellen sich widersprechen, steht die Spanne mit "wer sagt was" daneben.

---

## 1. Deckbau-Methoden und Zielzahlen

### 1.1 Die gängigen Templates im Vergleich

| Kategorie | Command Zone 2025 ("New Era", Folge 658) | 8x8-Methode | EDHREC Upgrade-Guide | EDHREC "How to Build" | 10/10/10 (Mythras) | "11 9s" (CoolStuffInc) | Nerd Leagues |
|---|---|---|---|---|---|---|---|
| Länder | **38** | 35 | – | 36–38 (mehr bei Commander-MV ≥ 5) | 37 | 36 | 36–38 |
| Ramp | **10** | 8 (+ Thema-Slots leihen) | ~10 (Minimum 7, Big Mana 15–20) | 8–12 | 10 | 9 | 8–12 |
| Kartenvorteil / Draw | **12** | 8 | 12+ | 8–10 | 10 | 9 | 10–12 |
| Gezielte Interaktion | **12** ("Targeted Disruption") | 8 Removal | ~10 Removal (Aggro 5–7, Control 15+) | 8–10 gesamt, davon 3–4 offensiv + 3–4 defensiv | 10 inkl. Wipes (~8 gezielt) | 9 | 8–10 inkl. Wipes |
| Massen-Interaktion / Wipes | **6** ("Mass Disruption") | 8 | mind. 2 | mind. 2 | 2–3 | (in Removal) | 2–3 |
| Schutz | (in Disruption) | 8 | – | – | (Flex) | – | – |
| Wincons | (in Plan-Karten) | (Thema-Paket "Finisher") | – | **mind. 7** | 1–3 Wege | (in Synergie) | – |
| Plan-/Synergie-/Themakarten | **30** | 4 Pakete à 8 = 32 | – | Rest | ~29–30 | 45 (Summe >99, Überlappung) | Rest |
| Tutoren | – | – | – | 1–2 zum Start, mehr bei höherem Power-Level | – | – | – |
| Friedhofshass | – | – | mind. 1 | 1–2 "Hate Cards" bei Bedarf | – | – | – |

Anmerkungen:
- Command Zone 2025: Die Kategorien summieren sich bewusst auf **108**, weil Karten mehrere Rollen erfüllen dürfen. Die Zahlen stammen aus der Community-Mitschrift des Templates; die Folge selbst behandelt Länder, Kartenvorteil, Ramp, Targeted Disruption, Mass Disruption, Plan Cards und Mana-Kurve. Kritik aus der Community: 6 Mass Disruption sei zu viel (lange Spiele), 18 Disruption insgesamt sei zu viel, 10 Ramp zu wenig (ein Vorschlag: ~13), 30 Plan-Karten zu wenig. Die Command Zone hat direkt danach eine Folge "The Problem with Deckbuilding Templates" (659) gemacht: Templates sind Startpunkt, kein Gesetz. [EDHREC – Command Zone 658](https://edhrec.com/articles/the-command-zone-commander-deckbuilding-template-for-the-new-era-the-command-zone-658-mtg-edh-magic-gathering), [r/EDH – Thoughts on the Command Zone's new template](https://axebps-redlib.hf.space/r/EDH/comments/1isxre2/thoughts_on_the_command_zones_new_deckbuilding), [EDHREC – Command Zone 659](https://edhrec.com/articles/the-command-zone-the-problem-with-deckbuilding-templates-the-command-zone-659-mtg-edh-magic-gathering)
- Altes Command-Zone-Template (Folge 379): laut Erinnerung eines Reddit-Kommentators etwa 34–36 Länder, 10 Ramp, 10 Draw, 10 Interaktion; das neue habe "ein paar Länder mehr". **Nur Sekundärquelle, unsicher.** [r/magicTCG – CommandZone new deck building template](https://axebps-redlib.hf.space/r/magicTCG/comments/1iyj5k3/commandzone_new_deck_building_template/mevxzh0)
- 8x8: 1 Commander + 35 Landslots + 8 Themen x 8 Karten = 100. Beispiel-Themen: Ramp, Draw, Removal, Wipes, Schutz + 4 Strategiepakete (z. B. Token-Erzeuger, Anthems, Sac-Payoffs, Finisher). Ramp und Draw dürfen über 8 gehen, die Slots werden aus den Strategiepaketen geliehen. Die gleiche Quelle empfiehlt allgemein 36–38 Länder, also mehr als die 35 der Methode. [Nerd Leagues – Ratios, Curves & the 8x8 Method](https://www.nerdleagues.com/blog/deck-building-basics-ratios-curves-the-8x8-method)
- EDHREC Upgrade-Guide nennt die Basis-Kategorien "Veggies". [EDHREC Guide to Upgrading Your Commander Deck](https://edhrec.com/guides/edhrec-guide-to-upgrading-your-commander-deck)
- EDHREC "How to Build": Wincons zuerst, dann Ramp, "Card Velocity", Interaktion, Länder, dann Extras (Recursion, Tutoren, Hate Cards). Ramp und Interaktion idealerweise 2–4 Mana. [EDHREC – How to Build a Commander Deck](https://edhrec.com/articles/how-to-build-a-commander-deck/)
- 10/10/10: [Mythras – How to Build a Commander Deck](https://gamertagmythras.com/blog/magic-the-gathering/how-to-build-a-commander-deck)
- "11 9s": Die Zahlen der Quelle addieren sich nicht sauber auf 99 → mit Vorsicht verwenden. [CoolStuffInc – Everything You Need to Know About Commander Deckbuilding](https://www.coolstuffinc.com/a/everything-you-need-to-know-about-commander-deckbuilding-05292026)

### 1.2 Was echte Decks tatsächlich spielen (Daten)

**EDHREC-Datenanalyse (MtGDS, Juli 2022), Mittelwert pro Deck, Kategorien über Scryfall-Tagger:**

| Funktion | Mittel | Median | % Decks mit ≥1 |
|---|---|---|---|
| Länder | 35,9 | 36 | – |
| Ramp | 12,7 | 12 | 99,5 % |
| Removal (gesamt) | 8,5 | 8 | 99,5 % |
| davon Kreatur-Removal | 5,1 | – | – |
| Draw | 7,6 | 7 | 99,1 % |
| Recursion | 4,7 | 4 | 93,4 % |
| Tutoren (ohne Länder) | 3,0 | 2 | 79,2 % |
| Sweeper (inkl. Schadens-Wipes) | 2,7 | 2 | 86,9 % |
| Counterspells | 2,4 | 1 | 54,0 % |

Kartentypen im Schnitt: 24,6 Kreaturen, 12,9 Artefakte, 10,0 Instants, 9,2 Sorceries, 8,5 Verzauberungen, 1,4 Planeswalker. Ein typischer 4er-Tisch sieht etwa 8 Sweeper insgesamt. [EDHREC – The Deck of Many Things](https://edhrec.com/articles/the-deck-of-many-things-card-frequencies-by-type-and-function-across-edh)

**Playgroup.gg-Template (Fünffarben, 18.018 Decks, 25.–75. Perzentil, wöchentlich aktualisiert, Kategorien über Scryfall-Oracle-Tags):**

| Kategorie | Niedrig | Typisch | Hoch |
|---|---|---|---|
| Länder | 35 | 37 | 38 |
| Ramp | 12 | 16 | 20 |
| Draw | 8 | 11 | 14 |
| Gezieltes Removal | 6 | 9 | 12 |
| Board Wipes | 1 | 3 | 4 |
| Counterspells | 0 | 1 | 2 |
| Schutz | 2 | 4 | 6 |
| Tutoren | 1 | 2 | 4 |
| Recursion | 2 | 3 | 6 |
| Friedhofshass | 0 | 1 | 1 |

Die Seite hat dieselben Bänder für 32 Farbidentitäten. Ein Wert außerhalb des Bandes ist ein Prüfhinweis, kein Fehler. Das ist ein gutes Vorbild für die App-Logik. [Playgroup – Deck Template](https://playgroup.gg/commander/deck-template)

**Ältere EDHREC-Zahl:** Ein durchschnittliches EDHREC-Deck spielte nur gut 29 Länder + ~4,15 Mana-Rocks; in neueren Decks waren es 31, in Precons über 37. Im Goldfish-Test mit 100 Zufallsdecks verpassten ~47 % den Landdrop in Zug 3 (26 % hatten auch keine andere Manaquelle). Der Autor nennt 29 Länder + 4 Rocks "far too anemic" außerhalb von cEDH. [EDHREC – Superior Numbers: Land Counts](https://edhrec.com/articles/superior-numbers-land-counts)

### 1.3 Länderanzahl: Formeln und Spannen

| Quelle | Empfehlung |
|---|---|
| **Frank Karsten** (Optimierungsmodell) | Start bei **42 Ländern + Sol Ring**; **−1 Land je 2–3 zusätzliche Mana-Rocks**; −1 Land je 3–4 billige Cantrips oder je 3–4 Mana-Dorks. Bei mittlerem Power-Level und Midrange **nicht unter 37**. |
| **Nate Burgess** (via EDHREC) | **Länder = 31 + Anzahl Farben + Commander-MV** (0-Mana-Rocks zählen als Länder). Für Nicht-cEDH. |
| ScrollVault (3,75 Mio. simulierte Spiele) | cEDH Turbo 29–31, Combo (Ø-MV 2,5) 33–35, Midrange (Ø-MV 3,0, 10 Ramp) 36–37, Battlecruiser (Ø-MV 3,5) 38–40, Landfall 38–40. Ab 37 flacht der Gewinn ab. |
| Playgroup.gg | 38–42 für typische Casual-Decks; niedrige Kurve/viel Draw 36–38; hohe Kurve 40–44. |
| Draftsim (A. Barker, 2026) | 33–41; Faustregel 2 Rocks ≈ 1 Land; 4–5 Farben 38–40; Mana-Sinks 39–42; Gesamt-Manaquellen 43–55. |
| CoolStuffInc (M. Gallagher, 2026) | 36–38 am häufigsten; Commander ≤ 4 MV: mind. 35 Länder + 9 Ramp; Commander ≥ 5 MV: bis 38 Länder + 10 Ramp; Bracket 5: ~23–29. |
| Command Zone 2025 | 38 |
| Gavin Verhey (zitiert bei SCG) | "39–40 minimum" in den meisten Decks |

Quellen: [ChannelFireball – Karsten: Optimal Mana Curve and Land/Ramp Count for Commander](https://strategy.channelfireball.com/home/whats-an-optimal-mana-curve-and-land-ramp-count-for-commander/), [EDHREC – Superior Numbers: Land Counts](https://edhrec.com/articles/superior-numbers-land-counts), [ScrollVault – Commander Land Count Data](https://scrollvault.net/guides/commander-land-count-data.html), [Playgroup – How Many Lands](https://playgroup.gg/commander/how-many-lands), [Draftsim – How Many Lands in Commander](https://draftsim.com/mtg-edh-deck-number-of-lands/), [CoolStuffInc – Building an Effective Mana Base](https://www.coolstuffinc.com/a/building-an-effective-mana-base-in-commander-08212026), [StarCityGames – Let's Talk About Lands Again](https://articles.starcitygames.com/select/lets-talk-about-lands-again/)

**ScrollVault-Wahrscheinlichkeiten (Midrange, Ø-MV 3,0, 10 Ramp):**

| Länder | 3-Drop in Zug 3 | 5-Drop in Zug 5 | 6-Drop in Zug 6 |
|---|---|---|---|
| 33 | 96,5 % | 93,1 % | 84,1 % |
| 37 | 97,2 % | 95,6 % | 90,3 % |
| 40 | 97,7 % | 96,8 % | 93,3 % |

Von 29 auf 37 Länder (mit 4 Rocks) steigt die Chance auf den 6-Drop pünktlich von 75,1 % auf 90,3 %. [ScrollVault](https://scrollvault.net/guides/commander-land-count-data.html)

**Effektive Länder (Schulze, Medium):** Nicht-Land-Ramp ≈ 0,75 Land, Cantrip ≈ 1/3 Land, Land-Suche = 1 Land. MDFCs laut ScrollVault mit Karsten-Werten: ungetappt ≈ 0,74 Land, getappt ≈ 0,38 Land. [Medium – The Math of Manabases in Commander](https://medium.com/@schulze.mtg/the-math-of-landbases-in-magic-the-gathering-commander-3f03aadac92c), [ScrollVault – Mana Bases](https://scrollvault.net/guides/mana-bases.html)

### 1.4 Farbquellen

Für 90 % Wahrscheinlichkeit (Karsten-Methodik, 99 Karten):
- 1 farbiges Pip in Zug 1: **~19–20 Quellen** (ScrollVault: 19; Schulze: 20).
- Doppel-Pip in Zug 2 (z. B. Counterspell): **~30 Quellen**.
- Rampant Growth in Zug 2: **19 grüne Quellen** (90 %) bzw. **23** (95 %).
- Vierfarben-Beispiel (Atraxa, Zug 4): **22 Quellen pro Farbe** für 95 %.

Karstens 99-Karten-Tabelle selbst (TCGplayer 2022) war für mich nicht abrufbar. Wer exakte Werte für C/1C/CC/2C/CCC braucht, sollte sie dort nachschlagen. [ScrollVault – Mana Bases](https://scrollvault.net/guides/mana-bases.html), [Medium – Schulze](https://medium.com/@schulze.mtg/the-math-of-landbases-in-magic-the-gathering-commander-3f03aadac92c), [Library of Leng – Karsten 2022 Update (Verweis)](https://library-of-leng.com/articles/tcgplayer-dc23a7d2-0a16-4c0b-ad36-586fcca03ad8)

**Manabasis nach Farbanzahl (CoolStuffInc):**

| Farben | Basics | Duals | Utility-Länder |
|---|---|---|---|
| 1 | ~14 (bis 20–30 bei Basic-Synergie) | – | mehr farblose Utility möglich |
| 2 | mind. 14 | mind. 13 | Platz für mehr |
| 3–4 | ~5–10 (bis 14 mit Farseek-artigem Ramp) | viel Fixing | mehr |
| 5 | z. B. 7 | z. B. 10 Fetches, 10 Shocks, Command Tower, 5–10 weitere | 0–4 |

Weitere Regeln: mindestens 1 Basic jeder Farbe; Budget-Decks höchstens ~4 Tapped Lands; höchstens 1 Draw-Land; Temple of the False God gilt als nie lohnend. Je mehr Farben, desto weniger farblose Utility-Länder (Draftsim: 4–5 Farben weitgehend vermeiden). [CoolStuffInc](https://www.coolstuffinc.com/a/building-an-effective-mana-base-in-commander-08212026), [Draftsim – Commander Mistakes](https://draftsim.com/mtg-commander-mistakes/)

### 1.5 Mana-Kurve und Commander-MV

**Karstens optimierte 99 nach Commander-MV:**

| Cmdr-MV | 1-Drops | 2 | 3 | 4 | 5 | 6 | Rocks | Länder |
|---|---|---|---|---|---|---|---|---|
| 2 | 9 | 0 | 20 | 14 | 9 | 4 | Sol Ring | 42 |
| 3 | 8 | 19 | 0 | 16 | 10 | 3 | Sol Ring | 42 |
| 4 | 6 | 12 | 13 | 0 | 13 | 8 | Sol Ring + 7 Signets | 39 |
| 5 | 6 | 12 | 10 | 13 | 0 | 10 | Sol Ring + 8 Signets | 39 |
| 6 | 6 | 12 | 10 | 14 | 9 | 0 | Sol Ring + 9 Signets | 38 |

Kernaussagen: Bei Commander mit MV 2–3 lohnen keine zusätzlichen Rocks; bei MV 4–6 lohnen 7–9 Signets. Auf dem MV des Commanders braucht man im Modell keine eigenen Karten. Das Modell enthält keinen Kartenzug; Karsten sagt selbst, dass Draw im echten Spiel mehr wert ist. Kleine Abweichungen von der Idealkurve kosten fast nichts. [ChannelFireball – Karsten](https://strategy.channelfireball.com/home/whats-an-optimal-mana-curve-and-land-ramp-count-for-commander/)

Weitere Kurvenregeln:
- Durchschnittliches MV um **3** anpeilen. [Mythras](https://gamertagmythras.com/blog/magic-the-gathering/how-to-build-a-commander-deck)
- Einsteigerdeck: Peak bei 2 und 3 Mana, dann abfallend; jede 5+-Karte muss beim Eintreffen sofort etwas tun. [Nerd Leagues](https://www.nerdleagues.com/blog/deck-building-basics-ratios-curves-the-8x8-method)
- "Always cut from the top": Laut Command-Zone-Statistik werden pro Spiel nur 1–2 Zauber mit MV 7+ gewirkt, also hat jeder Spieler nur ~25 % Chance, überhaupt einen zu wirken. Ausnahmen: Decks, die Kosten umgehen oder große Kreaturen reanimieren. [Commander's Herald – Always Cut From The Top](https://commandersherald.com/mechanical-engineering-always-cut-from-the-top/)
- cEDH-Decks liegen bei Ø-MV 1,68–2,04, normale Decks bei 3+. [EDHREC – Superior Numbers](https://edhrec.com/articles/superior-numbers-land-counts)

### 1.6 Wie sich die Zahlen verschieben (Regeln für die App)

| Situation | Anpassung | Quelle |
|---|---|---|
| Commander-MV ≥ 5 | mehr Länder (bis 38+) und ~10 Ramp, eher Rocks | Karsten, CoolStuffInc, EDHREC |
| Commander-MV ≤ 3 | kaum Extra-Rocks, mehr 1–2-Drops | Karsten |
| Landfall | 38–40 Länder, Ramp als Land-Ramp | ScrollVault, Mythras |
| Viel Draw/Cantrips | −1 Land je 3–4 Cantrips; 33–35 Länder möglich | Karsten, Draftsim |
| Viele Rocks | −1 Land je 2–3 Rocks | Karsten, Draftsim |
| Mana-Sinks / X-Spells | 39–42 Länder | Draftsim |
| Aggro | Removal 5–7 reicht | EDHREC Upgrade-Guide |
| Control | Removal 15+ | EDHREC Upgrade-Guide |
| Big Mana / Ramp-Deck | Ramp 15–20 | EDHREC Upgrade-Guide |
| Synergie-lastig (z. B. Aristocrats) | weniger reaktive Karten, mehr Engine | Reddit-Kritik am CZ-Template |
| Self-Mill / Friedhof | weniger klassischer Draw nötig | CoolStuffInc |
| Bracket 5 / cEDH | 23–31 Länder, Ø-MV ~2 | CoolStuffInc, ScrollVault, EDHREC |

### 1.7 Wie Profis vorgehen (Ansätze)

- **Game Plan zuerst:** "How do I win?" ist die erste Frage. Wincons rein, dann Support. Jede Karte bekommt eine Hauptrolle, dann wird die Kurve gelegt und ein **Turn Mapping** gemacht (in welchem Zug spiele ich die Karte realistisch?). [EDHREC – How to Build](https://edhrec.com/articles/how-to-build-a-commander-deck/)
- **Plan in einem Satz:** 1–3 Wincon-Routen, primärer Plan als ein Satz. [Mythras](https://gamertagmythras.com/blog/magic-the-gathering/how-to-build-a-commander-deck)
- **Bau-Einstiege:** Farbe zuerst (typisch cEDH), Mechanik zuerst (am verbreitetsten), Hybrid (Strategie + Farben, dann passender Commander), Lieblingsfigur zuerst (tendiert zu Bracket 1). [EDHREC – Different Approaches](https://edhrec.com/articles/different-approaches-to-building-a-commander-deck)
- **Workflow mit Tools:** EDHREC-Seite des Commanders ("Top Cards", "High Synergy"), Archidekt für Kategorien und Kosten/Produktion, Commander Spellbook für Combos. [EDHREC – Digital Deckbuilding](https://edhrec.com/articles/digital-deckbuilding-the-how-to-guide-to-building-a-commander-deck-using-edhrec-archidekt-and-commander-spellbook), [EDHREC – How to Build](https://edhrec.com/articles/how-to-build-a-commander-deck/)
- **Ownership:** Ein befriedigendes Deck hat (1) eine klare Identität, (2) persönliche Handschrift (Lieblingskarten, auch leichte Downgrades) und (3) genug Power für den eigenen Tisch. [Card Kingdom – The Secret to a Satisfying Commander Deck](https://blog.cardkingdom.com/the-secret-to-a-satisfying-commander-deck/)
- Command Zone, Game Knights, Tolarian Community College und Salubrious Snail: Ihre konkreten Zahlen habe ich nur bei der Command Zone verlässlich gefunden. Für die anderen gab es keine textlich zitierbaren Zahlen, deshalb erfinde ich keine.

---

## 2. Offizielles Commander-Bracket-System (Stand Nov. 2026)

### 2.1 Zeitachse

| Datum | Änderung |
|---|---|
| 11.02.2025 | Beta-Start, 40 Game Changers |
| 22.04.2025 | Großer Zuwachs an Game Changers (u. a. Consecrated Sphinx, Humility, Necropotence, Orcish Bowmasters, Teferi's Protection, Survival of the Fittest); Unbans als Game Changer (Braids, Coalition Victory, Gifts Ungiven, Panoptic Mirror) |
| 21.10.2025 | Brackets bekommen Erwartungen + Mindest-Zuganzahl; **Tutor-Regel komplett gestrichen**; Bracket 2 nicht mehr "Precon-Bracket"; Game Changers gestrichen: Expropriate, Jin-Gitaxias Core Augur, Sway of the Stars, Vorinclex Voice of Hunger, Kinnan, Urza, Winota, Yuriko, Deflecting Swat, Food Chain |
| 09.02.2026 | **Farewell** neu (Bracket 3+), **Biorhythm** (unbanned) als Game Changer; Lutri nicht aufgenommen; Hybrid-Regel bleibt unverändert; nächstes Update für Mai/Juni 2026 angekündigt, "Beta"-Label könnte 2026 fallen |

Ein Bracket-Update nach Februar 2026 konnte ich nicht in einer Primärquelle finden. Die Game-Changer-Liste unten ist am 23.11.2026 von Playgroup aus Scryfall synchronisiert und deckt sich mit Draftsims Stand vom 19.05.2026. [WotC – Brackets Beta Update Feb 9, 2026](https://magic.wizards.com/en/news/announcements/commander-brackets-beta-update-february-9-2026), [WotC – Update Oct 21, 2025](https://magic.wizards.com/en/news/announcements/commander-brackets-beta-update-october-21-2025), [WotC – Update Apr 22, 2025](https://magic.wizards.com/en/news/announcements/commander-brackets-beta-update-april-22-2025), [Draftsim – Game Changers](https://draftsim.com/mtg-edh-game-changers/), [Draftsim – Oct 2025 Changes](https://draftsim.com/mtg-october-2025-commander-bracket-changes/)

### 2.2 Die fünf Brackets

| Bracket | Name | Absicht | Wincons | Mind. Züge | Game Changers | Mass Land Denial | Extra Turns | 2-Karten-Combos |
|---|---|---|---|---|---|---|---|---|
| 1 | Exhibition | Thema/Idee vor Power; Regeln dürfen flexibel sein (z. B. Un-Karten); Deck "vorzeigen" | sehr thematisch oder unterdurchschnittlich | **9** | keine (thematische Ausnahmen, z. B. Bolas's Citadel in Bolas-Deck, vorher absprechen) | nein | nein | nein |
| 2 | Core | unoptimiert, geradlinig, kreative Kartenwahl; sozial, wenig Druck | inkrementell, sichtbar am Board, störbar | **8** | keine | nein | einzelne ok, **kein Chaining** | nein |
| 3 | Upgraded | starke Synergie, hohe Kartenqualität, kann stören | in einem großen Zug aus der Hand nach Aufbau | **6** | **max. 3** | nein | kein Chaining | **nicht vor Zug 6** |
| 4 | Optimized | tödlich, konsistent, schnell; nicht auf cEDH-Meta gebaut | effizient, fast sofort | **4** | frei | frei | frei | frei |
| 5 | cEDH | auf cEDH-Meta gebaut | maximal effizient | jeder Zug | frei | frei | frei | frei |

- Die Zuganzahlen sind ein fester Richtwert. Ein einzelner Verstoß wirft ein Deck aber nicht automatisch aus seinem Bracket.
- Tutoren haben seit Oktober 2025 keine eigene Regel mehr; die effizientesten stehen auf der Game-Changer-Liste.
- Bracket 3 ist bewusst breit. Ein sechstes Bracket wurde diskutiert, aber nicht eingeführt.
- Brackets sind ein Gesprächswerkzeug. Gemischte Spiele (2 vs. 3, 3 vs. 4) können gut funktionieren; vermeiden sollte man vor allem 2 gegen 4.

[EDHREC Guide to Commander Brackets](https://edhrec.com/guides/edhrec-guide-to-commander-brackets), [WotC – Oct 21, 2025](https://magic.wizards.com/en/news/announcements/commander-brackets-beta-update-october-21-2025), [Draftsim – Commander Power Bracket](https://draftsim.com/mtg-commander-power-bracket/), [WotC – Introducing Commander Brackets Beta](https://magic.wizards.com/en/news/announcements/introducing-commander-brackets-beta), [WotC – Feb 9, 2026](https://magic.wizards.com/en/news/announcements/commander-brackets-beta-update-february-9-2026)

**Definitionen (offiziell):**
- **Mass Land Denial:** Karten, die mehrere Länder zerstören, exilieren oder bouncen, Länder getappt halten oder das Mana von vier oder mehr Ländern pro Spieler ändern, ohne sie zu ersetzen. Beispiele: Armageddon, Ruination, Sunder, Winter Orb, Blood Moon.
- **Extra Turns:** Ein einzelner Extra-Turn-Zauber ist ok. Chaining oder Looping gilt als Combo und ist in 1–3 verboten. In 1–2 nur in geringer Menge.
- **2-Karten-Combo:** nicht formal definiert. Gemeint sind Combos aus zwei Karten, die das Spiel beenden, locken oder unendlich sind (Beispiel: Thassa's Oracle). In 1–3 nicht absichtlich. Ein versehentlich entdecktes Combo disqualifiziert nicht, sollte aber für künftige Spiele entfernt werden.
- **Game-Changer-Kriterien:** beste Tutoren, effiziente Lock-Effekte, starkes Fast Mana, Snowball-Ressourcenvorteil, Combo-/Storm-Karten, Win-on-the-spot- oder Reset-Effekte, bestimmte Commander, freie Counterspells.

[WotC – Introducing Commander Brackets Beta](https://magic.wizards.com/en/news/announcements/introducing-commander-brackets-beta)

### 2.3 Aktuelle Game-Changer-Liste (53 Karten)

Stand 23.11.2026 laut Playgroup (aus Scryfall `is:gamechanger` synchronisiert), deckt sich mit Draftsim (19.05.2026). [Playgroup – Game Changers](https://playgroup.gg/commander/game-changers), [Draftsim – Game Changers](https://draftsim.com/mtg-edh-game-changers/)

| Farbe | Karten |
|---|---|
| Weiß (6) | Drannith Magistrate, Enlightened Tutor, Farewell, Humility, Smothering Tithe, Teferi's Protection |
| Blau (10) | Consecrated Sphinx, Cyclonic Rift, Fierce Guardianship, Force of Will, Gifts Ungiven, Intuition, Mystical Tutor, Narset, Parter of Veils, Rhystic Study, Thassa's Oracle |
| Schwarz (10) | Ad Nauseam, Bolas's Citadel, Braids, Cabal Minion, Demonic Tutor, Imperial Seal, Necropotence, Opposition Agent, Orcish Bowmasters, Tergrid, God of Fright // Tergrid's Lantern, Vampiric Tutor |
| Rot (3) | Gamble, Jeska's Will, Underworld Breach |
| Grün (6) | Biorhythm, Crop Rotation, Natural Order, Seedborn Muse, Survival of the Fittest, Worldly Tutor |
| Mehrfarbig (4) | Aura Shards, Coalition Victory, Grand Arbiter Augustin IV, Notion Thief |
| Farblos (14) | Ancient Tomb, Chrome Mox, Field of the Dead, Gaea's Cradle, Glacial Chasm, Grim Monolith, Lion's Eye Diamond, Mana Vault, Mishra's Workshop, Mox Diamond, Panoptic Mirror, Serra's Sanctum, The One Ring, The Tabernacle at Pendrell Vale |

**Für die App:** Die Liste nicht hart codieren, sondern regelmäßig per Scryfall `is:gamechanger` abfragen (siehe Abschnitt 7).

### 2.4 Selbsteinschätzung (Algorithmus)

1. **Absicht prüfen:** Wofür ist das Deck gebaut? Die Absicht ist das wichtigste Kriterium.
2. **Game Changers zählen:** 0 → Bracket 1–2 möglich; 1–3 → mind. Bracket 3; > 3 → mind. Bracket 4. Ein Game-Changer-Commander zählt mit und ist in 1–2 verboten.
3. **MLD prüfen:** vorhanden → mind. Bracket 4.
4. **Extra Turns:** mehrere oder Loops (z. B. mit Recursion) → mind. Bracket 4; einzelne → ok ab Bracket 2.
5. **2-Karten-Combos:** in 1–2 keine; in 3 nur, wenn sie realistisch nicht vor Zug 6 zünden; sonst Bracket 4.
6. **Erwartete Spieldauer schätzen:** Gewinnt das Deck regelmäßig vor Zug 6 (bzw. 8 oder 9)? Dann eine Stufe höher.
7. **Gesamt-Power:** Auch ohne Game Changers kann ein Deck in Bracket 4 gehören.
8. **Ergebnis als Startpunkt** fürs Gespräch nutzen, nicht als Urteil. Das Deck gehört in das niedrigste Bracket, dessen Kriterien es erfüllt.

[Draftsim – Commander Power Bracket](https://draftsim.com/mtg-commander-power-bracket/), [WotC – Introducing](https://magic.wizards.com/en/news/announcements/introducing-commander-brackets-beta)

Werkzeuge mit automatischer Schätzung: Commander Spellbook (Bracket-Tab in Find My Combos), TableCommander, Draftsim- und Playgroup-Bracket-Rechner. TableCommander: Ohne Signal → Bracket 1; jedes Signal hebt den Boden; eine 2-Karten-Combo ist mind. Bracket 3, und Bracket 4, wenn beide Teile plus Ausführung **≤ 5 Mana** kosten oder Spellbook sie als "Ruthless" führt. Echte MLD → Bracket 4. Die MLD-Liste wurde von 16 auf 99 Karten erweitert (inkl. Soft-Locks und Mana-Umschreibern; ohne Planeswalker-Ultimates und ohne From the Ashes). [TableCommander – Bracket Estimates Rebuilt](https://tablecommander.com/blog/bracket-estimates-rebuilt), [Playgroup – Bracket Calculator](https://playgroup.gg/commander/bracket-calculator), [Draftsim – Bracket Calculator](https://draftsim.com/edh-power-level)

### 2.5 Das Rule-0-Gespräch

**Was ist Rule 0:** eine inoffizielle Absprache vor dem Spiel. Regeländerungen gelten nur, wenn **alle** zustimmen; lehnt einer ab, gilt das offizielle Regelwerk. Wer ein angepasstes Deck mitbringt, sagt es an und hat ein Ersatzdeck dabei. [Draftsim – Rule 0](https://draftsim.com/rule-0-commander-mtg/)

**Gesprächsleitfaden (für die App als Spickzettel):**
- "Ich spiele Bracket X, außer dieser einen Sache. Ist das ok für euch?" [WotC – Introducing](https://magic.wizards.com/en/news/announcements/introducing-commander-brackets-beta)
- "Ich habe N Game Changers im Deck. Passt das?"
- Grober Game Plan und Wincon ("Ich gewinne über Token und einen Overrun-Effekt").
- Combos? Infinite? Extra Turns? Stax?
- Proxies, Un-Karten, gebannte Karten?
- Grenzen der anderen (z. B. "bitte keine Infinite Combos").
- Mulligan-Regel am Tisch.
- Nach dem Spiel: Was hat Spaß gemacht? Das ist die Grundlage fürs nächste Gespräch.

[Rule 0 Conversations](https://rule0.carrd.co/), [Draftsim – Rule 0](https://draftsim.com/rule-0-commander-mtg/), [Commander's Herald – Above and Beyond Rule 0](https://commandersherald.com/above-and-beyond-rule-0/)

---

## 3. Infinite Combos

### 3.1 Combo-Kategorien

| Typ | Prinzip | Beispiele |
|---|---|---|
| Infinite Mana | Quelle tappen/untappen mit Netto-Plus | Grand Architect + Pili-Pala; Selvala + Freed from the Real; Devoted Druid + Vizier of Remedies; Deadeye Navigator + Peregrine Drake |
| Infinite Schaden/Leben | Pingen/Draining in Schleife | Duskmantle Guildmage + Mindcrank; Sorin, Vengeful Bloodlord + Famished Paladin + Sorcerer's Wand |
| Infinite Kreaturen/Token | Kopier- oder Blink-Loop mit Haste | Kiki-Jiki + Deceiver Exarch; Riku of Two Reflections + Palinchron |
| Infinite Counters | Counter-Loop | Enduring Scalelord + Altered Ego |
| Infinite Turns | Extra-Turn-Zauber recyceln | Temur Sabertooth + Time Warp + Archaeomancer |
| Sonstiges | Draw/Cast, Mill, ETB/LTB-Loops | Enter the Infinite + Omniscience |
| Alternative Siegbedingung | "win the game" bei leerer Bibliothek | Thassa's Oracle (+ Selbst-Exil der Bibliothek) |

**Typischer Aufbau:** 2–4 Karten. Eine **Engine** wiederholt etwas, ein **Payoff** macht daraus den Sieg (z. B. Mana → Kartenzug → Schaden). Gegner können meist in die Schleife reagieren. Eine Schleife ohne Ende und ohne Ausstieg ist ein Unentschieden. Draftsim: 2-Karten-Combos schieben ein Deck Richtung Bracket 4–5, Combos aus 3+ Karten passen eher in Bracket ≤ 3. Das ist eine Vereinfachung; offiziell zählt "nicht vor Zug 6". [Draftsim – MTG Infinite Combos](https://draftsim.com/mtg-infinite-combos/)

### 3.2 Combos erkennen (Logik für die App)

1. Deckliste an Commander Spellbook "Find My Combos" schicken.
2. Spellbook liefert drei Gruppen: **schon im Deck**, **fast im Deck** (1+ Karte fehlt) und **mit anderer Farbidentität oder anderem Commander möglich**. Dazu kommt ein Tab mit Bracket-Schätzung und Begründung. [EDHREC – How to Use Commander Spellbook](https://edhrec.com/articles/how-to-use-commander-spellbook-the-combo-search-engine)
3. Jede Combo hat einen **Bracket-Tag**: `Ruthless` (R, → 4), `Spicy` (S, → 3), `Powerful` (P, → 3), `Oddball` (O, → 2), `Core` (C, → 2), `Exhibition` (E, → 1), `Banned` (B). Die Tags werden automatisch erzeugt und sind ein Richtwert. [Commander Spellbook – Syntax Guide](https://commanderspellbook.com/syntax-guide)
4. Weitere Filter: `is:winning`, `is:lock`, `is:mld`, `is:tutor`, `is:extraturn`, `is:gamechanger`, `cards<=2`, `result:infinite`, `pre<=3` (Voraussetzungen), `popularity>1000`, `salt>2.5`, `bracket<=2`, `ci:` für Farbidentität. [Commander Spellbook – Syntax Guide](https://commanderspellbook.com/syntax-guide)
5. App-Regel (CLAUDE.md): Combos **nur markieren, nie automatisch einbauen**.

### 3.3 Wann ist eine Combo ok?

| Bracket | Combo-Regel | Coach-Empfehlung |
|---|---|---|
| 1 | keine 2-Karten-Combos | nur thematische Mehrkarten-Interaktionen, vorher ansagen |
| 2 | keine 2-Karten-Combos, keine Infinites | Combo-Funde als Warnung anzeigen und Entfernen vorschlagen |
| 3 | 2-Karten-Combos erst ab Zug 6 realistisch | billige Combos (≤ 5 Mana gesamt) oder "Ruthless" warnen; Tutoren für Combo-Teile prüfen |
| 4–5 | frei | trotzdem im Rule-0-Gespräch ansagen |

[EDHREC Guide to Brackets](https://edhrec.com/guides/edhrec-guide-to-commander-brackets), [TableCommander](https://tablecommander.com/blog/bracket-estimates-rebuilt)

### 3.4 Combos am Tisch ansprechen

- Vorher sagen: "Mein Deck hat eine Infinite Combo (X + Y), die frühestens um Zug ~7 zündet. Ok?" [Rule 0 Conversations](https://rule0.carrd.co/)
- **Absicht vs. Zufall:** Eine zufällig entdeckte Combo disqualifiziert nicht, sollte aber danach entfernt werden. [WotC – Introducing](https://magic.wizards.com/en/news/announcements/introducing-commander-brackets-beta)
- Combo kurz erklären, eine Schleife anzeigen und dann abkürzen ("Ich mache das 1000-mal").
- Weniger explosive Alternative: Combos so bauen, dass die Teile **Permanents am Board** sind. Dann sieht jeder, wie nah ein Sieg ist, und kann reagieren. [Card Kingdom – How to Keep Commander Less Explosive](https://blog.cardkingdom.com/how-to-keep-commander-less-explosive/)

---

## 4. Spaßfaktor

### 4.1 Was Commander spaßig macht

Sheldon Menery nennt fünf Gründe: (1) soziales Spiel, (2) herausfordernder Deckbau mit Themen, (3) Karten, die man sonst nie sieht (Hidden Gems), (4) Karten, die man sonst nie spielen darf, (5) epische Boardstates und Comebacks. Sein Leitsatz: **"build casually, play competitively"**. Mass Land Destruction und Prison meiden, weil sie Spiele für andere elend machen. [StarCityGames – What Makes Commander Fun](https://articles.starcitygames.com/articles/what-makes-commander-fun/)

**Regeln für ein "spaßiges" Deck:**
- **Interaktion ja, aber dosiert:** Eher gezieltes Removal statt vieler Wipes. Das hält Spiele interaktiv, ohne dass ständig alle zurückgesetzt werden. [StarCityGames – Your Commander Motivation](https://articles.starcitygames.com/magic-the-gathering/your-commander-motivation-and-how-it-shapes-your-magic-games/)
- **Keine Solitaire-Züge:** Lange Solo-Züge frustrieren den Tisch. [EDHREC – The Art of Balance](https://edhrec.com/articles/the-art-of-balance-in-commander-gameplay)
- **Abwechslung statt Tutoren:** Tutoren machen Spiele gleichförmig. Besser "Smoother" (Looting, Scry, Draw), die Ressourcen finden, ohne gezielt zu suchen. [EDHREC – The Art of Balance](https://edhrec.com/articles/the-art-of-balance-in-commander-gameplay)
- **Schrittweiser Druck statt One-Turn-Kill:** Engines, die über mehrere Züge Wert erzeugen. [Card Kingdom – Less Explosive](https://blog.cardkingdom.com/how-to-keep-commander-less-explosive/)
- **Swingy, situative Karten** schaffen Geschichten (Chaos Wand, Dualcaster Mage, Vernal Equinox); Stalemate-Brecher (Coveted Jewel, Hostile Negotiations) halten Spiele in Bewegung. [Card Kingdom – Optimize for Fun](https://blog.cardkingdom.com/its-time-to-optimize-for-fun-in-commander/)
- Für längere, interaktivere Spiele: weniger billiger Ramp, mehr Ramp im späteren Spiel (z. B. Solemn Simulacrum); bei der Kartenwahl fragen: "Will this make the game more fun?" [StarCityGames – Your Commander Motivation](https://articles.starcitygames.com/magic-the-gathering/your-commander-motivation-and-how-it-shapes-your-magic-games/)
- **Ownership:** Lieblingskarten dürfen rein, auch wenn sie leichte Downgrades sind. [Card Kingdom – Satisfying Deck](https://blog.cardkingdom.com/the-secret-to-a-satisfying-commander-deck/)

### 4.2 Salt: Was Karten unangenehm macht

**Salt Score:** jährliche Community-Umfrage, Bewertung 0 (nicht salzig) bis 4 (sehr salzig). Der Score ist der **Durchschnitt aller Stimmen**. Archidekt zeigt eine **Salt Sum** (Summe über alle Karten im Deck). Salt hat **keinen Zusammenhang mit Brackets oder Game Changers**. [EDHREC – How to Use EDHREC](https://edhrec.com/guides/how-to-use-edhrec), [EDHREC FAQ](https://edhrec.com/faq)

**Salt 2026 (veröffentlicht 16.10.2026, ~2,2 Mio. Stimmen), Top 10:**

| # | Karte | Salt |
|---|---|---|
| 1 | Stasis | 3,05 |
| 2 | Armageddon | 2,98 |
| 3 | Winter Orb | 2,93 |
| 4 | The Tabernacle at Pendrell Vale | 2,83 |
| 5 | Rhystic Study | 2,82 |
| 6 | Tergrid, God of Fright | 2,81 |
| 7 | Grand Arbiter Augustin IV | 2,76 |
| 8 | Vivi Ornitier | 2,71 |
| 9 | Static Orb | 2,71 |
| 10 | Ravages of War | 2,63 |

Dominierende Kategorien: Stax/Steuern, Mass Land Destruction, Ressourcen- und Such-Verweigerung (z. B. Stranglehold), "Pay the 1"-Steuern. Die vollständige Liste steht unter [edhrec.com/top/salt](https://edhrec.com/top/salt). [EDHREC – Salt Vote Results 2026](https://edhrec.com/articles/salt-vote-results-2026)

**Vier Gründe, warum Karten sich schlecht anfühlen:**
1. Sie erzeugen uneinholbare Vorsprünge.
2. Sie blockieren normales Spielen (Stax: Untap, Zaubern, Mana).
3. Sie sind zu stark für Casual-Tische (Combos, Top-Commander).
4. Sie löschen Entscheidungen (Chaos-Resets von Board oder Hand).

Salt ist **keine Banliste**. Man sollte salzige Karten vorher ansagen, zum Tisch passend wählen und kann bewusst den "Bösewicht" spielen, wenn der Tisch das will. [EDHREC – Salt Isn't a Ban List](https://edhrec.com/articles/salt-isnt-a-ban-list)

### 4.3 Spielertypen (Psychographics) → Decktyp

| Typ | Was ihn antreibt | Passende Decktypen | Fallstricke |
|---|---|---|---|
| **Timmy/Tammy** | große, spektakuläre Momente | Big Mana/Ramp, Dinosaurier/Drachen, Big Creatures, X-Spells, Overrun | wenig Removal, langsamer Aufbau |
| **Johnny/Jenny** | Synergie, Combos, Ausdruck, "mein Weg" | Engine-Decks, Aristocrats, Blink, Spellslinger, ungewöhnliche Commander, Mehrkarten-Combos | trifft weder maximale Geschwindigkeit noch maximale Power |
| **Spike** | gewinnen, Effizienz | optimierte Combo-, Control- oder Turbo-Decks (Bracket 4–5) | repetitiv, für Gegner oft unangenehm |
| **Vorthos** | Story, Art, Lore | Flavor-, Charakter- und Storytelling-Decks, Typal nach Welt oder Figur | eher Casual, weniger Siegfokus |
| **Melvin/Melanie** | Regeln, Interaktionen, Mechanik | Stack-Tricks, Layer-Interaktionen, ungewöhnliche Mechaniken | komplexe Stacks, Wincon manchmal unklar |

EDHREC-Ergänzungen: **Turtle** (Pillow Fort, Group Hug: Propaganda, Ghostly Prison, Phelddagrif, Kynaios and Tiro), **Goblin Diplomat** ("I attack you with everything": Kaalia, Saskia, Zurgo), **Puppet Master** (Politik, Manipulation: Zedruu, Edric, Mathas), **Barktooth** (obskure Commander), **Herm** (≈ Spike, Combos, Land Destruction). [EDHREC – Different Approaches](https://edhrec.com/articles/different-approaches-to-building-a-commander-deck), [EDHREC – An Introduction to EDH Player Psychographics](https://edhrec.com/articles/an-introduction-to-edh-player-psychographics), [WotC – Timmy, Johnny and Spike Revisited](https://magic.wizards.com/en/news/making-magic/timmy-johnny-and-spike-revisited-2006-03-20)

### 4.4 Power-Level vs. Spaß

- Auf reine Power optimierte Decks werden linear und rigide. Frust und Burnout entstehen oft durch Spiele ohne Höhen und Tiefen. Empfehlung: **auf Spaß und Varianz optimieren** und Lieblings-Commander wählen statt Tier-Liste. [Card Kingdom – Optimize for Fun](https://blog.cardkingdom.com/its-time-to-optimize-for-fun-in-commander/)
- Gegenposition: Zu casual zu sein (sich aus dem gemeinsamen Spielziel ausklinken) ist genauso unbefriedigend wie zu kompetitiv. Entscheidend ist, dass alle **dieselben Erwartungen** haben. [EDHREC – The Art of Balance](https://edhrec.com/articles/the-art-of-balance-in-commander-gameplay)
- Ein Deck muss am eigenen Tisch mithalten können, darf ihn aber nicht überrollen. [Card Kingdom – Satisfying Deck](https://blog.cardkingdom.com/the-secret-to-a-satisfying-commander-deck/)

---

## 5. Archetypen-Katalog

Spaß und Komplexität sind **Einschätzungen** (1 = niedrig, 5 = hoch); "Spaß gegen" meint, wie angenehm der Archetyp typischerweise für Gegner ist. Spielpläne und Beispiele stammen aus [Playgroup – Archetypes](https://playgroup.gg/commander/archetypes), [Draftsim – Commander Archetypes](https://draftsim.com/?p=175821) und [CoolStuffInc – Types of Decks in Commander](https://www.coolstuffinc.com/a/types-of-decks-in-commander-06232026).

| Archetyp | Spielplan | Schlüsselrollen | Typische Wincons | Stärken | Schwächen | Spaß selbst / gegen | Komplexität | Farben (typisch) | Beispiel-Commander |
|---|---|---|---|---|---|---|---|---|---|
| **Aggro** | früh angreifen, Schaden über Kampf/Burn | viele billige Kreaturen, Haste, Anthems; kaum etwas über 4 MV | Kampfschaden | schneller Druck | Wipes; 3 Gegner à 40 Leben sind viel | 4 / 3 | 2 | R, W, RW | Adeline, Isshin, Tovolar |
| **Voltron** | Equipment/Auren auf eine Kreatur, meist Commander | Equipment, Auren, Schutz (Hexproof, Indestructible), Evasion | 21 Commander-Schaden | schnell, fokussiert | gezieltes Removal, Edicts; wird Hauptziel | 4 / 3 | 2 | W, R, WU, RW | Galea, Nahiri, Geist of Saint Traft |
| **Tokens / Go-Wide** | Board fluten, dann ein großer Angriff | Token-Erzeuger, Anthems, Overrun-Finisher | Alpha Strike, Drain | resilient gegen Spot-Removal | Wipes; ohne genug Token-Effekte keine kritische Masse | 4 / 3 | 2 | W, G, GW, RW | Neyali, Jinnie Fay, Kasla |
| **Aristocrats** | opfern für Wert, Todes-Trigger drainen den Tisch | Sac-Outlets, Fodder, Death-Payoffs (Blood Artist) | Drain bei allen Gegnern | resilient gegen Wipes | Friedhofshass; viele Trigger | 4 / 3 | 3–4 | B, BW, BR, Mardu | Teysa Karlov, Endrek Sahr, Nethroi |
| **Spellslinger** | viele Instants/Sorceries + Payoffs | billige Spells, Payoffs (Guttersnipe, Archmage Emeritus), Kopien | Burn-Payoffs, große Copy-Züge | instant-schnell, interaktiv | wenige Kreaturen; lange Züge möglich | 4 / 3 | 4 | U, R, UR | Feather, Kraum, Urabrask |
| **Reanimator / Friedhof** | Friedhof füllen, Bestes zurückholen | Self-Mill, Discard, Reanimate, Recursion | große reanimierte Kreatur | spart Mana, sehr flexibel | Friedhofshass | 4 / 3 | 3–4 | B, BG, UB | Mirko, Sidisi, Kagha |
| **Landfall** | Länder sind mehr als Mana | Extra-Landdrops, Land-Ramp, Landfall-Payoffs, Utility-Länder | Token/Schaden über Landfall | Ramp ist gleich Synergie | braucht 38–40 Länder | 4 / 4 | 3 | G, GU, Naya | Tatyova, Obuun, Omnath |
| **+1/+1 Counters** | Kreaturen wachsen lassen, Proliferate | Counter-Verdoppler (Hardened Scales), Proliferate | Kampfschaden | viele Support-Karten | Wipes | 4 / 4 | 2–3 | G, GW, Simic | Bright-Palm, Hamza, Shalai and Hallar |
| **Artefakte** | Artefakte, ETB-Payoffs, Treasures | Rocks, Payoffs, Sac-Outlets, Tutoren | artefaktspezifische Wincons | beliebtester Archetyp auf EDHREC (laut Draftsim) | Artefakt-Wipes | 4 / 3 | 3–4 | U, R, farblos | Armix, Urtet, Chiss-Goria |
| **Enchantress** | Verzauberungen spielen, dafür ziehen | Enchantress-Engines, Auren, Pillow Fort | Engine-Overload, Pillow Fort + Angriff | sehr viel Kartenzug | Verzauberungs-Wipes | 4 / 3 | 3 | GW, Abzan | Anikthea, Marina Vendrell |
| **Typal (Tribal)** | ein Kreaturentyp + Lords | Lords, Typal-Support (Herald's Horn, Cavern of Souls) | Alpha Strike mit Lords | einsteigerfreundlich, starker Flavor | Wipes; teils schwache Einzelkarten | 5 / 4 | 2 | je Typ | The Ur-Dragon, Sliver Gravemother, Ezuri, Muxus |
| **Group Hug** | allen helfen, damit einen niemand angreift | symmetrische Effekte (Howling Mine), versteckte Wincons | Politik, versteckte Combos | sozial, gesprächig | der stärkste Gegner profitiert am meisten | 3 / 5 | 3 | GU, Esper, Bant | Kynaios and Tiro, Phelddagrif, Gluntch |
| **Group Slug** | alle schaden, sich selbst auch | Symmetrische Burn-/Life-Loss-Effekte (Sulfuric Vortex, Painful Quandary) | alle sterben, man selbst zuletzt | Druck auf alle | wird früh gemeinsam bekämpft | 3 / 2 | 2–3 | R, BR | Mogis, Torbran, Ojer Axonil |
| **Control** | überleben, Bedrohungen beseitigen, spät gewinnen | Counter, Removal, Wipes, Flash | Engine oder Finisher | wird mit der Zeit stärker | zu wenige Antworten → überrannt; zu viele → kein Sieg | 3 / 2 | 4 | U, UB, UW, Esper | Y'shtola, Queen Marchesa |
| **Stax** | Gegner einschränken (Steuern, Untap, Mana) | Stax-Teile (Winter Orb, Torpor Orb), asymmetrisch brechen | Lock + kleine Wincon | stoppt Combo | Top-Salt-Kategorie, an Casual-Tischen verpönt | 3 / 1 | 4–5 | W, U, farblos | Derevi, Lavinia, Hokori |
| **Combo** | bestimmte Karten zusammenbringen, sofort gewinnen | Combo-Teile, Tutoren, Draw/Dig, Schutz | Combo | gewinnt plötzlich | Removal und Counter; bracket-kritisch | 3 / 2 | 4–5 | alle, oft U/B | K'rrik, Vivi Ornitier |
| **Big Mana / Ramp** | früh Mana, riesige Bedrohungen vor der Zeit | Dorks, Rampant Growth, Rocks, Finisher | große Kreaturen, X-Spells | spektakulär (Timmy) | Wipes; Mittelspiel kann leer sein | 5 / 3 | 2 | G, Gx | Pantlaza, Ellie and Alan |
| **Blink** | ETB-Effekte wiederverwenden | Blink-Engines (Soulherder, Teleportation Circle), ETB-Kreaturen | Wert-Overload, Drain-ETBs | Werte-Engine | Torpor Orb; wenig Removal-Platz | 4 / 3 | 3–4 | W, U, Bant | Lagrella, Roon, Niko |
| **Wheels** | Hände abwerfen und neu ziehen | Windfall, Wheel of Fate, Draw-/Discard-Payoffs | Schaden durch Draw-Trigger | viele Angriffswinkel | hilft Gegnern auch | 4 / 3 | 3 | UR, Temur, BR | Xyris, Nekusar |
| **Mill** | Bibliotheken leeren | Mill-Karten, Mill-Verdoppler | leere Bibliothek | ungewöhnlicher Siegweg | 3 Bibliotheken à ~90 Karten; Shuffle-Effekte | 3 / 3 | 2–3 | U, UB | Phenax, Bruvac, The Mindskinner |
| **Politics / Goad / Monarch** | Gegner gegeneinander lenken | Goad, Votes, Monarch, Deals | Gegner reiben sich auf | sehr sozial | abhängig vom Tisch | 4 / 4 | 3–4 | R, U, Jeskai, Mardu | Nelly Borca, Firkraag, Zedruu |
| **Chaos** | Unvorhersehbarkeit maximieren | Coin Flips, Warp World, Kontrollwechsel | oft keine echte | Geschichten | ineffizient, "Erasing decisions" kann salzig sein | 5 / 3 | 3 | UR, R | Okaun, Yusri, Karona |
| **Cascade / Discover** | freie Zauber durch Cascade | Cascade-Enabler, MV-Struktur | Board-Overload | Varianz + Wert | Kurvenbau nötig | 4 / 3 | 3 | Temur, Jund, 4c | Yidris, Maelstrom Wanderer |
| **Lifegain** | Leben in Karten, Counter oder Schaden verwandeln | Lifegain-Payoffs (Sanguine Bond), Aetherflux Reservoir | Drain, Reservoir | schwer zu töten | Payoffs teils langsam | 4 / 3 | 2 | W, WB | Oloro, Liesa |

**Zusätzliche Fun-/Casual-Formen:**
- **Pillow Fort:** Angriffe besteuern (Propaganda, Ghostly Prison). [EDHREC – Psychographics](https://edhrec.com/articles/an-introduction-to-edh-player-psychographics)
- **False Hug:** Ressourcen geben und für deren Nutzung bestrafen (Nekusar, Kibo). [CoolStuffInc – Types of Decks](https://www.coolstuffinc.com/a/types-of-decks-in-commander-06232026)
- **Theft:** gegnerische Karten nutzen (Evelyn, Gonti). [Draftsim – Archetypes](https://draftsim.com/?p=175821)
- **Storytelling/Flavor-Decks, Budget-Challenges, "Jank":** passen zu Bracket 1–2. Lieblingsfigur zuerst tendiert zu Bracket 1. [EDHREC – Different Approaches](https://edhrec.com/articles/different-approaches-to-building-a-commander-deck)
- **Infect:** bewusst schwächer als der Schnitt und unbeliebt. [Draftsim – Archetypes](https://draftsim.com/?p=175821)

---

## 6. Lehransatz: Fehler, Testen, Bewerten, Kürzen, Upgraden

### 6.1 Typische Anfängerfehler (Warnregeln)

| Fehler | Erkennungsregel (Vorschlag) | Quelle |
|---|---|---|
| Zu wenige Länder | < 36 (Warnung) bzw. < 33 (kritisch), außer Ø-MV < 2,5 | Draftsim (≥ 36), Karsten (≥ 37), ScrollVault |
| Kurve zu hoch | Ø-MV > 3,5 oder > 12 Karten mit MV ≥ 5 ohne passende Ramp | Draftsim, Nerd Leagues, Commander's Herald |
| Keine/zu wenig Interaktion | gezieltes Removal < 5; keine Artefakt-/Verzauberungs-Antwort; kein Friedhofshass | Draftsim, EDHREC Upgrade |
| Keine Wipes | 0 Wipes (außer Go-Wide-/Aggro-Deck bewusst) | EDHREC Upgrade (mind. 2) |
| Kein Wincon | < 7 Karten, die den Plan beenden | EDHREC How to Build |
| Self-Hoser / Non-Bos | symmetrischer Kreatur-Wipe im Kreaturendeck; Nonbasic-Hate bei gieriger Manabasis | Draftsim |
| Veraltete "Staples" | teure Karten ohne Board-Effekt | Draftsim |
| Zu viele farblose Länder | 4–5 Farben + farblose Utility-Länder | Draftsim |
| Zu wenig Kartenzug | Draw < 8 | Templates (8–12) |
| Viele Einzelkarten ohne Synergie | Synergie-Score niedrig, keine Kategorie ≥ 6 Karten | Card Kingdom (Identität), CoolStuffInc (Synergie > Einzelpower) |

[Draftsim – Commander Mistakes](https://draftsim.com/mtg-commander-mistakes/), [EDHREC Upgrade Guide](https://edhrec.com/guides/edhrec-guide-to-upgrading-your-commander-deck), [EDHREC – How to Build](https://edhrec.com/articles/how-to-build-a-commander-deck/), [MTGGoldfish – Three Biggest Commander Deck Building Mistakes](https://www.mtggoldfish.com/articles/brewer-s-minute-three-biggest-commander-deck-building-mistakes)

### 6.2 Playtesten und Goldfishen

- **Mulligan-Regel:** Erster Mulligan im Multiplayer **gratis**; danach legt man pro weiterem Mulligan eine Karte mehr unter die Bibliothek. Faustregel: nie unter 5 Karten. Viele Gruppen spielen per Hausregel mit unbegrenzten Mulligans. [EDHREC – Guide to Mulligans](https://edhrec.com/articles/the-edhrec-guide-to-mulligans-in-commander)
- **Behaltbare Hand:** passende Farben, Kurve passt zum Deck, die Hand verfolgt den Plan, eine Bedrohung bis ca. Zug 4. 2 Länder sind meist ein Mulligan-Kandidat. [EDHREC – Guide to Mulligans](https://edhrec.com/articles/the-edhrec-guide-to-mulligans-in-commander)
- **Reale Daten (Playgroup):** Bei 250.943 Starthänden hatten 89 % der behaltenen Hände 2–4 Länder (Ø 2,96). 64 % der Spiele hatten keinen Mulligan, ein Spiel dauerte im Mittel 8,7 Runden (Median 9). [Playgroup – How Many Lands](https://playgroup.gg/commander/how-many-lands)
- **Goldfish-Protokoll (Vorschlag für die App, aus den Quellen abgeleitet):** 10 Starthände ziehen → Behalten/Mulligan begründen → 5–7 Züge solo spielen → pro Zug notieren: Landdrop? Mana genutzt? Commander in welchem Zug? Was blieb in der Hand stecken? EDHRECs Goldfish-Kennzahl: **Landdrop in Zug 3 verpasst** (siehe 1.2). [EDHREC – Superior Numbers](https://edhrec.com/articles/superior-numbers-land-counts), [TappedOut – EDH Deck Building Process #6: Playtesting](https://tappedout.net/mtg-articles/2020/may/2/edh-deck-building-process-6-playtesting-and-asking)
- **Echte Spiele:** Annahmen prüfen. Wird man von einer Strategie abgeschaltet, eine gezielte Antwort ergänzen (z. B. Disenchant). [EDHREC – How to Build](https://edhrec.com/articles/how-to-build-a-commander-deck/)
- **Sideboard:** Gekürzte Karten als "Maybeboard" behalten und zwischen Spielen tauschen. [EDHREC – How to Cut Cards](https://edhrec.com/articles/new-player-guide-how-to-cut-cards-from-your-commander-decks)

### 6.3 Karten bewerten: Fragenkatalog

1. **Bringt sie den Spielplan voran?** Sie sollte entweder den Plan voranbringen, helfen, wenn etwas schiefgeht, oder ein gutes Board in einen Sieg verwandeln. [EDHREC Upgrade Guide](https://edhrec.com/guides/edhrec-guide-to-upgrading-your-commander-deck)
2. **Welche Hauptrolle hat sie?** (Ramp, Draw, Removal, Wipe, Schutz, Wincon, Synergie) Doppelrollen sind ein Plus. [EDHREC – How to Build](https://edhrec.com/articles/how-to-build-a-commander-deck/), [CoolStuffInc](https://www.coolstuffinc.com/a/everything-you-need-to-know-about-commander-deckbuilding-05292026)
3. **In welchem Zug spiele ich sie realistisch?** (Turn Mapping)
4. **Passt die Ramp/Draw-Art zum Deck?** (Landfall → Rampant Growth; Artefakte → Mind Stone) [EDHREC – How to Build](https://edhrec.com/articles/how-to-build-a-commander-deck/)
5. **Skaliert sie im Multiplayer?** Removal sollte billig sein oder mehrere Gegner treffen. [Draftsim – Mistakes](https://draftsim.com/mtg-commander-mistakes/)
6. **Schadet sie mir selbst?** (Non-Bo-Check)
7. **Passt sie zum Ziel-Bracket?** (Game Changer? Combo-Teil? MLD? Extra Turn?)
8. **Salt-Check:** Ist sie für meinen Tisch unangenehm? Dann ansagen oder ersetzen. [EDHREC – Salt Isn't a Ban List](https://edhrec.com/articles/salt-isnt-a-ban-list)
9. **Hate Cards** sollten auch dann nützlich sein, wenn sie nicht gebraucht werden (z. B. Soul-Guide Lantern). [EDHREC – How to Build](https://edhrec.com/articles/how-to-build-a-commander-deck/)
10. **Macht sie mir Spaß?** Lieblingskarten haben ihren Platz. [Card Kingdom – Satisfying Deck](https://blog.cardkingdom.com/the-secret-to-a-satisfying-commander-deck/)

### 6.4 Karten kürzen (auf 100 kommen)

1. Ein Template als Basis nehmen (z. B. Command Zone mit 38 Ländern).
2. Länder beiseitelegen und als festes Fundament behandeln.
3. Nichtland-Slots nach den Template-Kategorien füllen.
4. **Eins-zu-eins tauschen**, nicht hektisch streichen (sonst verzählt man sich).
5. Erste Kandidaten: mehr Rocks, Ramp oder Disruption, als der Commander braucht; redundante oder langsamere Versionen derselben Funktion.
6. **Von oben kürzen:** teure Karten zuerst.
7. Ein paar Länder kürzen ist ok, besonders in Zweifarben- und Aggro-Decks.
8. Testen, dann mit dem Sideboard nachjustieren.

[EDHREC – How to Cut Cards](https://edhrec.com/articles/new-player-guide-how-to-cut-cards-from-your-commander-decks), [Commander's Herald – Always Cut From The Top](https://commandersherald.com/mechanical-engineering-always-cut-from-the-top/), [EDHREC Upgrade Guide](https://edhrec.com/guides/edhrec-guide-to-upgrading-your-commander-deck)

### 6.5 Precon-Upgrade-Pfad

1. **Basis prüfen:** Ramp ~10, Removal ~10, Kartenvorteil 12+, Wipes ≥ 2, Friedhofshass ≥ 1.
2. **Überschuss kürzen:** z. B. zu viel 3-Mana-Land-Ramp (Cultivate, Kodama's Reach), langsamere Doppelungen.
3. **Lücken füllen:** meist Removal und Draw.
4. **Auf das Ziel-Bracket abstimmen:** Karten, die nicht ins Ziel-Bracket passen, raus (in beide Richtungen).
5. **High-Impact-Karten** ergänzen, die den Plan beschleunigen oder abschließen.

Budget-Tipp: zuerst Ramp, Kartenzug und Manabasis verbessern; Einzelkarten kaufen statt Sealed-Produkt. Precons spielen im Schnitt über 37 Länder. [EDHREC Upgrade Guide](https://edhrec.com/guides/edhrec-guide-to-upgrading-your-commander-deck), [Mythras](https://gamertagmythras.com/blog/magic-the-gathering/how-to-build-a-commander-deck), [EDHREC – Precon Upgrade Guide Feature](https://edhrec.com/articles/new-edhrec-feature-precon-upgrade-guide), [EDHREC – Superior Numbers](https://edhrec.com/articles/superior-numbers-land-counts)

### 6.6 Spielfehler, die der Coach erklären kann

Instants und Flash-Karten auf Sorcery-Speed spielen; Treasures vor Ländern nutzen; unbekannte Karten nicht lesen; Angriffsziel auswürfeln statt Bedrohungen einzuschätzen; mit dem Führenden paktieren; bei Rhystic Study nicht "the 1" zahlen; Bedrohungen nur nach Leben oder Kreaturenzahl beurteilen statt nach Mana und Karten. [Draftsim – Commander Mistakes](https://draftsim.com/mtg-commander-mistakes/)

---

## 7. Datenquellen für die App

### 7.1 Scryfall

- **Rate Limits:** `/cards/search`, `/cards/named`, `/cards/random`, `/cards/collection` → **2 Requests/s (500 ms)**; alle anderen Endpunkte → **10/s (100 ms)**; `*.scryfall.io` (Bilder, Bulk) → ohne Limit. HTTP 429 sperrt für 30 s; wer 429 ignoriert, riskiert einen Bann. [Scryfall – Rate Limits](https://scryfall.com/docs/api/rate-limits)
- **Caching:** mind. 24 h. Für Massenabfragen die täglichen Bulk-Dateien nutzen. Gameplay-Daten reicht es, wöchentlich oder nach Set-Release zu laden. (CLAUDE.md: Cache 3 Tage, passt.) [Scryfall – Rate Limits](https://scryfall.com/docs/api/rate-limits)
- **Header:** Scryfall verlangt laut eigenem Blog einen `User-Agent`- und `Accept`-Header. [Scryfall Blog – User-Agent and Accept header now required](https://scryfall.com/blog/category/api), [Scryfall – API Documentation](https://scryfall.com/docs/api)
- **Nützliche Felder:** `color_identity`, `legalities.commander`, `edhrec_rank`, `produced_mana`, `keywords`. Die Card-Object-Doku listet **kein** `game_changer`-Feld. Deshalb per Suche `is:gamechanger` ermitteln und das JSON im Projekt einmal real prüfen. [Scryfall – Card Objects](https://Scryfall.com/docs/api/cards)
- **Suchoperatoren:**
  - `is:gamechanger` (Game Changers)
  - `is:commander` (darf Commander sein), `is:partner`
  - `f:commander` (legal), `banned:commander`
  - `id:` / `identity:` (Farbidentität, auch Gilden-, Shard- und Wedge-Namen), `id<=sultai`
  - `otag:` / `oracletag:` / `function:` (Tagger-Funktionstags)
  - `mv=`, `produces=`, `kw:`, `edhrec:` / `order:edhrec`
  - [Scryfall – Search Reference](https://scryfall.com/docs/syntax)
- **Belegte otag-Namen:** `otag:ramp`, `otag:removal`, `otag:card-advantage`, `otag:mill`, `otag:mill-self`, `otag:mill-opponent`, `otag:synergy-mill`, `otag:pp-counters-matter`, `otag:gives-pp-counters`. Beispiel: `otag:ramp commander:sultai legal:edh order:edhrec`. [EDHREC – Guide to Scryfall Syntax](https://edhrec.com/articles/guide-to-scryfall-syntax)
  - Weitere Tags wie Wipe, Tutor, Counterspell, Recursion oder Schutz existieren laut Playgroup und EDHREC-Analysen (beide nutzen Scryfall-Tagger-Kategorien). Ihre **exakten Tag-Namen konnte ich nicht verifizieren**. Vor Nutzung auf tagger.scryfall.com prüfen (Kandidaten: `sweeper`/`board-wipe`, `tutor`, `counterspell`, `recursion`, `draw`).

### 7.2 EDHREC

- Keine offizielle API und keine Aussage zu Scraping oder App-Nutzung in der FAQ. [EDHREC FAQ](https://edhrec.com/faq)
- Die Website lädt Daten aus JSON-Seiten (Community-Tools wie Cockatrice nutzen das, z. B. Average-Deck-Statistiken mit Feldern `creature`, `instant`, `sorcery`, `artifact`, `enchantment`, `battle`, `planeswalker`, `land`, `basic`, `nonbasic`). [Cockatrice – EdhrecCommanderApiResponseAverageDeckStatistics](https://cockatrice.github.io/docs/d8/d0f/structEdhrecCommanderApiResponseAverageDeckStatistics.html)
- Die oft genannten URLs `json.edhrec.com/pages/commanders/<slug>.json` und `json.edhrec.com/pages/average-decks/<slug>.json` konnte ich aus der Sandbox **nicht live prüfen** (kein Netz). Sie sind inoffiziell und können sich ändern.
- Inhalte auf der Website: Commander-Seiten mit Top Cards, High Synergy, Filtern nach Bracket, Budget und Tags; Themes- und Kindred-Tag-Seiten; Average Deck; Salt Score (Ø 0–4); Inclusion (Decks mit beiden Karten / mögliche Decks). [EDHREC – How to Use EDHREC](https://edhrec.com/guides/how-to-use-edhrec), [EDHREC FAQ](https://edhrec.com/faq)
- Empfehlung: sparsam cachen, auf EDHREC verlinken, nicht massenhaft abfragen.

### 7.3 Commander Spellbook

- Open Source (MIT), Django-Backend mit REST-API; offizieller TS-Client `@space-cow-media/spellbook-client`. [GitHub – commander-spellbook-backend](https://github.com/SpaceCowMedia/commander-spellbook-backend)
- Basis-URL in Drittclients: `https://backend.commanderspellbook.com`. Endpunkte (laut Client-Code und Doku):
  - `GET /variants?q=...&limit=&offset=` (Combo-Suche mit Syntax aus 3.2)
  - `GET|POST /find-my-combos` (Deck → Combos; POST mit `DeckRequest`-Body)
  - `POST /card-list-from-text` (Text-Deckliste parsen, `text/plain`)
  - `GET /cards`, `GET /cards/{id}`
  - [Glama – scryfall-connector csb.ts](https://glama.ai/mcp/servers/@latte-chan/scryfall-connector/blob/c715c801679c7c0ea17e144879b5384636e289cd/src/csb.ts), [spellbook-client – FindMyCombosApi](https://unpkg.com/@space-cow-media/spellbook-client@5.4.10/spellbook-client/docs/FindMyCombosApi.md)
- Das Schema von `DeckRequest` (vermutlich Listen `main`/`commanders`) und die Antwortfelder (Gruppen "included" / "almost included") sind in den abgerufenen Seiten nicht dokumentiert. Vor der Implementierung am OpenAPI-Schema des Backends prüfen. Eine explizite Rate-Limit- oder Nutzungsbedingung habe ich nicht gefunden. Höflich cachen.

### 7.4 Archidekt / Moxfield

- **Archidekt:** Die API ist offen lesbar, aber ohne offizielle Doku oder Support. Beispiel `GET https://archidekt.com/api/decks/<id>/`. Bedingungen laut Staff: auf Archidekt zurückverlinken und Deck-Autoren nennen; bei Problemen wird die API gesperrt. Kein Rate Limit genannt. Archidekt bietet Kategorien pro Karte und eine Kosten-/Produktionsübersicht (Farbquellen-Check). [Archidekt Forum – API To Query Deck](https://archidekt.com/forum/thread/40353), [EDHREC – How to Build](https://edhrec.com/articles/how-to-build-a-commander-deck/)
- **Moxfield:** keine öffentliche, dokumentierte API gefunden; Nutzer fordern sie im Feedback-Board. Für die App am besten Import per Text-Export statt API. [Moxfield Feedback – Open API](https://moxfield.nolt.io/1431)
- **Playgroup.gg:** Vorbild für Template-Bänder je Farbidentität und Bracket-Rechner (keine API-Recherche). [Playgroup – Deck Template](https://playgroup.gg/commander/deck-template)

---

## 8. Für die App

### (a) Geführter Bau-Flow mit Fragen

| Schritt | Ziel | Fragen an den Spieler (mit Beispielantworten zur Inspiration) | App-Logik |
|---|---|---|---|
| 0. Spielertyp | Decktyp-Vorschlag | Fragebogen (d) | Profil → 2–3 Archetyp-Vorschläge |
| 1. Tisch und Bracket | Ziel-Power festlegen | "Wie spielt deine Gruppe? Precons, aufgerüstete Decks, Turnier-Combos?" / "Wie lange sollen Spiele dauern?" (z. B. "1–2 h, mind. 8 Züge") / "Sind Combos, Stax, Extra Turns ok?" | Ziel-Bracket 1–5 setzen; Regeln aus 2.2 aktivieren |
| 2. Commander | Farben + Mechanik | "Willst du von einem Commander, einer Strategie, einer Farbe oder einer Lieblingsfigur ausgehen?" / "Welche Commander besitzt du schon?" | `is:commander id<=...`; Game-Changer-Commander in Bracket 1–2 blocken |
| 3. Game Plan in einem Satz | Siegweg festlegen | "Wie gewinnst du? Beispiel: 'Ich baue viele Token und gewinne mit einem Overrun-Effekt.'" / "Welcher Moment soll sich großartig anfühlen?" | Plan-Text speichern; 1–3 Wincon-Routen wählen |
| 4. Wincons | ≥ 7 Karten, die den Plan beenden | "Welche Karten beenden das Spiel für dich?" | Zähler Wincon; Combo-Check (Spellbook) |
| 5. Thema/Synergie | 25–35 Plan-Karten | "Welche Kartentypen oder Mechaniken sollen tragen?" | EDHREC-High-Synergy + `otag:`-Suchen; Besitz (Collectr, `physical`) bevorzugen |
| 6. Ramp | 8–12 (je nach Commander-MV) | "Wie teuer ist dein Commander? Willst du früh große Dinge tun?" | Ramp-Ziel nach 1.6; passende Ramp-Art vorschlagen |
| 7. Kartenvorteil | 10–12 | "Bevorzugst du Engines (wiederholt) oder einmalige Draw-Spells?" | Repeatable vor One-Shot |
| 8. Interaktion | 8–12 gezielt + 2–4 Wipes | "Wie viel willst du auf Gegner reagieren? Wipes im eigenen Kreaturendeck?" | Non-Bo-Check; Artefakt-/Verzauberungs-Removal + Friedhofshass prüfen |
| 9. Schutz | 2–6 | "Ist dein Commander der Plan? Dann brauchst du Schutz." | Voltron/Commander-zentriert → höher |
| 10. Länder und Manabasis | 33–42 (Formel) | "Wie viele Farben, wie viele Rocks/Dorks?" | Karsten + Burgess anzeigen; Farbquellen je Pip |
| 11. Kurve und Turn Mapping | Ø-MV ~3 | "Was spielst du in Zug 2, 3 und 4?" | Kurven-Chart; Warnung bei Kopflastigkeit |
| 12. Kürzen auf 100 | Eins-zu-eins | "Welche Karte tut am wenigsten für deinen Plan?" | von oben kürzen; Redundanz markieren |
| 13. Bracket-Check | Ehrliche Einstufung | – | Algorithmus 2.4 + Spellbook |
| 14. Salt- und Spaß-Check | Tisch-Verträglichkeit | "Gibt es Karten, die du ansagen solltest?" | Salt Sum; Top-Salt-Karten markieren |
| 15. Goldfish | Konsistenz | "Behältst du diese Hand? Warum?" | 10 Starthände, 5–7 Züge, Statistik |
| 16. Rule-0-Spickzettel | Ansage | – | Bracket, Game-Changer-Zahl, Combos, Plan in einem Satz |

### (b) Kategorie-Checkliste mit Zielbereichen

| Kategorie | Minimum (Warnung darunter) | Zielbereich | Obergrenze (Hinweis darüber) | Herleitung |
|---|---|---|---|---|
| Länder | 33 (kritisch), 36 (Warnung) | Formel: Karsten 42 − Rocks/2,5 bzw. 31 + Farben + Cmdr-MV; meist 36–38 | 42 (außer Landfall/Sinks) | 1.3 |
| Ramp | 7 | 8–12 (Big Mana 15–20) | 20 | EDHREC Upgrade, Templates, Playgroup |
| Kartenvorteil | 8 | 10–12 | 15 | CZ 12, EDHREC 12+, Nerd Leagues 10–12 |
| Gezieltes Removal | 5 | 8–12 | 15+ nur Control | EDHREC, CZ |
| Board Wipes | 1 (0 nur bewusst bei Go-Wide/Aggro) | 2–4 | 6 (CZ-Wert, Community hält ihn für hoch) | EDHREC, CZ, Playgroup |
| Schutz | 0 (Voltron: 3) | 2–6 | – | Playgroup |
| Wincons | 3 (kritisch), 7 empfohlen | 7+ | – | EDHREC How to Build |
| Plan-/Synergiekarten | 20 | 25–35 | – | CZ 30, 8x8 32 |
| Friedhofshass | 0 → Hinweis | 1–2 | – | EDHREC Upgrade, Playgroup |
| Tutoren | – | Bracket 1–2: 0–2 (Smoother bevorzugen); 3: 1–3 | Game Changer zählen | EDHREC How to Build, Art of Balance |
| Recursion | – | 2–6 | – | Playgroup |
| Ø-MV (ohne Länder) | – | ~2,8–3,2 | > 3,5 Warnung | Mythras, ScrollVault |
| Karten MV ≥ 7 | – | 0–3 | > 4 Warnung (außer Cheat/Reanimator) | Commander's Herald |
| Farbquellen | 1 Pip früh: ≥ 19; CC früh: ≥ 30 (oft unrealistisch → Karte überdenken) | – | – | 1.4 |
| Tapped Lands | – | ≤ 4 | > 4 Hinweis | CoolStuffInc |

### (c) Warnregeln (Wenn → Dann)

**Mana**
- `Länder < 33` → **Kritisch:** "Unter 33 Ländern verpasst du sehr oft Landdrops. In EDHRECs Test verpassten 47 % den Drop in Zug 3."
- `Länder < 36 und Ø-MV ≥ 3` → Warnung mit Formelwert.
- `Länder > 42 und keine Landfall-/Sink-Karten` → Hinweis "Flood-Risiko".
- `Commander-MV ≥ 5 und Ramp < 10` → Warnung.
- `Farben ≥ 4 und farblose Utility-Länder > 2` → Warnung.
- `Farbquellen für Farbe X < 19 und Karten mit X-Pip auf MV ≤ 2 vorhanden` → Warnung.
- `Tapped Lands > 4` → Hinweis.
- `Karten mit MV ≥ 7 > 4 ohne Cheat-/Reanimator-Thema` → "Von oben kürzen."

**Interaktion**
- `Board Wipes = 0` → Warnung "keine Brettwischer" (abschwächen bei Go-Wide/Aggro mit Begründung).
- `Gezieltes Removal < 5` → Warnung.
- `kein Artefakt-/Verzauberungs-Removal` → Hinweis.
- `kein Friedhofshass` → Hinweis.
- `symmetrischer Kreatur-Wipe und Kreaturen > 30` → Non-Bo-Hinweis.

**Plan**
- `Wincons < 3` → Kritisch "kein klarer Siegweg".
- `Kartenvorteil < 8` → Warnung.
- `keine Kategorie/kein Thema mit ≥ 6 Karten` → Hinweis "viele Einzelkarten ohne Synergie".

**Bracket** (Ziel-Bracket = B)
- `B ≤ 2 und Game Changer ≥ 1` → Kritisch (Karte nennen).
- `B = 3 und Game Changer > 3` → Kritisch.
- `Commander ist Game Changer und B ≤ 2` → Kritisch.
- `B ≤ 2 und 2-Karten-Combo im Deck` → **Kritisch "Combo in Bracket 2"** (Teile nennen, Entfernen vorschlagen, nie automatisch).
- `B = 3 und Combo Ruthless oder ≤ 5 Mana gesamt` → Warnung "zündet vermutlich vor Zug 6".
- `B ≤ 3 und MLD-Karte` → Kritisch.
- `B ≤ 3 und ≥ 2 Extra-Turn-Karten oder Extra Turn + Recursion` → Warnung "Chaining".
- `B ≤ 2 und ≥ 1 Extra-Turn-Karte` → Hinweis "in geringer Menge ok, ansagen".
- `B ≤ 2 und Tutoren > 2` → Hinweis "Abwechslung leidet; Smoother erwägen".

**Spaß/Salt**
- `Karte in Salt-Top-100` → Hinweis "im Rule-0-Gespräch ansagen".
- `Salt Sum hoch` → Hinweis. (Schwelle nicht aus einer Quelle; empirisch festlegen.)
- `Stax-Teile in B ≤ 2` → Warnung.

### (d) Fragebogen zum Decktyp

Jede Frage hat Beispielantworten; die App zählt Punkte pro Archetyp.

1. **"Welcher Moment in einem Spiel macht dich am glücklichsten?"**
   - a) "Ein riesiges Monster auf den Tisch knallen." → Big Mana, Typal (Drachen/Dinos), Big Creatures (Timmy)
   - b) "Wenn meine Engine läuft und alles ineinandergreift." → Aristocrats, Blink, Spellslinger, Artefakte (Johnny)
   - c) "Gewinnen, egal wie." → Combo, Control (Spike, höheres Bracket)
   - d) "Wenn mein Deck eine Geschichte erzählt." → Flavor/Typal/Storytelling (Vorthos)
   - e) "Eine komplizierte Regelinteraktion durchziehen." → Melvin-Decks, Stack-lastiger Spellslinger
2. **"Wie willst du mit den anderen am Tisch umgehen?"**
   - a) "Alle angreifen, jede Runde." → Aggro, Tokens, Voltron (Goblin Diplomat)
   - b) "Deals machen, andere gegeneinander lenken." → Politics, Goad, Monarch (Puppet Master)
   - c) "Allen etwas geben, damit mich niemand angreift." → Group Hug, Pillow Fort (Turtle)
   - d) "Am liebsten in Ruhe aufbauen." → Enchantress, Landfall, Control
3. **"Wie viel Glück und Chaos magst du?"**
   - a) "Je verrückter, desto besser." → Chaos, Cascade/Discover, Coin Flips
   - b) "Etwas Varianz ist gut." → die meisten Synergie-Decks
   - c) "Ich will Kontrolle." → Control, Tutor-lastiger, eher höheres Bracket
4. **"Wie komplex darf dein Zug sein?"**
   - a) "Einfach: Karte spielen, angreifen." → Aggro, Voltron, Typal, Tokens (Komplexität 2)
   - b) "Ein paar Trigger sind ok." → +1/+1 Counters, Landfall, Lifegain
   - c) "Gerne viele Trigger und Stack-Entscheidungen." → Aristocrats, Spellslinger, Blink, Wheels
5. **"Wie soll das Spiel enden?"**
   - a) "Kampf und Commander-Schaden." → Voltron, Aggro
   - b) "Ein großer Angriff mit vielen Kreaturen." → Tokens, Typal
   - c) "Alle verlieren gleichzeitig Leben." → Aristocrats, Group Slug, Lifegain-Drain
   - d) "Eine clevere Combo." → Combo (Bracket-Hinweis!)
   - e) "Ungewöhnlich, z. B. Mill oder Poison." → Mill, Infect
6. **"Was ist für dich ein schlechtes Spiel?"**
   - a) "Wenn ich nichts machen darf." → kein Stax/MLD im eigenen Deck; Pillow Fort meiden
   - b) "Wenn es nach Zug 5 vorbei ist." → Bracket 2–3
   - c) "Wenn es 3 Stunden dauert." → weniger Wipes, schnellere Wincons
   - d) "Wenn ich ohne Chance verliere." → mehr Interaktion
7. **"Welche Farben oder Figuren magst du?"** (offen; Beispiele: "Grün, ich liebe Dinos", "Alles mit Vampiren", "Mein Lieblingscharakter aus Lord of the Rings")
8. **"Was hast du schon an Karten oder Precons?"** → Besitz-Daten aus Collectr und Precons; Archetyp mit größter Abdeckung höher gewichten.
9. **"Budget?"** (z. B. "nur Karten, die ich habe", "bis 50 €", "egal")
10. **"Wie spielt deine Gruppe?"** → Ziel-Bracket (siehe Flow, Schritt 1).

**Auswertung (Vorschlag):** Top 3 Archetypen nach Punkten. Dazu je ein "Warum passt das zu dir"-Satz, die Komplexität und der "Spaß gegen"-Wert aus Abschnitt 5 und ein Beispiel-Commander. Combo und Stax nur vorschlagen, wenn das Ziel-Bracket ≥ 3 ist und Frage 6a nicht gewählt wurde.

---

## Offene Punkte und Unsicherheiten

- Ob es nach dem 09.02.2026 ein weiteres Bracket- oder Game-Changer-Update gab, konnte ich nicht über eine Primärquelle bestätigen. Die Liste vom 23.11.2026 (Playgroup/Scryfall) enthält 53 Karten. In der App per `is:gamechanger` live halten.
- Karstens exakte 99-Karten-Farbquellen-Tabelle (TCGplayer 2022) war nicht abrufbar. Nur Einzelwerte sind belegt.
- Die Zahlen des alten Command-Zone-Templates (Folge 379) sind nur aus zweiter Hand.
- Exakte Scryfall-otag-Namen für Wipes, Tutoren, Counter, Schutz und Recursion sind nicht verifiziert. EDHREC-JSON und das Spellbook-Request-Schema konnten wegen fehlenden Netzes in der Sandbox nicht live getestet werden.
- Für Game Knights, Tolarian Community College, Commander's Quarters und Salubrious Snail fand ich keine textlich zitierbaren Zahlen-Templates.
