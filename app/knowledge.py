"""Deckbau-Wissen für den Coach.

Quelle: research/commander-wissen.md (Recherche Nov. 2026; Command Zone 2025, EDHREC, Karsten,
Playgroup, ScrollVault, WotC-Bracket-Updates bis 09.02.2026). Zahlen sind Richtwerte, keine Gesetze.
"""

# ---------------------------------------------------------------- Zielbereiche
# (kritisch_unter, ziel_von, ziel_bis, hinweis_über)
TARGETS = {
    "lands": (33, 36, 38, 42),
    "ramp": (7, 8, 12, 20),
    "draw": (8, 10, 12, 15),
    "removal": (5, 8, 12, 15),
    "wipe": (1, 2, 4, 6),
    "protection": (0, 2, 6, 99),
    "wincon": (3, 7, 12, 99),
    "synergy": (20, 25, 35, 99),
}

ROLE_LABELS = {
    "land": "Land",
    "ramp": "Ramp",
    "draw": "Kartenvorteil",
    "removal": "Gezieltes Removal",
    "wipe": "Brettwischer",
    "protection": "Schutz",
    "wincon": "Wincon",
    "synergy": "Plan/Synergie",
    "tutor": "Tutor",
    "recursion": "Recursion",
    "gravehate": "Friedhofshass",
}


def adjusted_targets(commander_mv: float, archetype: str | None, colors: int) -> dict:
    """Zielbereiche an Commander-Kosten, Farben und Archetyp anpassen (Regeln 1.6 der Recherche)."""
    t = {k: list(v) for k, v in TARGETS.items()}
    # Burgess-Formel für Länder: 31 + Farben + Commander-MV, eingeklammert auf 35–40
    burgess = max(35, min(40, round(31 + colors + (commander_mv or 0))))
    t["lands"][1], t["lands"][2] = burgess - 1, burgess + 1
    if commander_mv and commander_mv >= 5:
        t["ramp"][1] = 10
    a = (archetype or "").lower()
    if a in ("big-mana",):
        t["ramp"][1:3] = [15, 20]
    if a in ("landfall",):
        t["lands"][1:3] = [38, 40]
    if a in ("aggro", "voltron"):
        t["removal"][1:3] = [5, 8]
    if a in ("control",):
        t["removal"][1:3] = [12, 18]
    if a in ("voltron",):
        t["protection"][0:3] = [3, 4, 8]
    if a in ("tokens", "aggro"):
        t["wipe"][0] = 0
    return {k: tuple(v) for k, v in t.items()}


# ---------------------------------------------------------------- Brackets
BRACKETS = {
    1: {"name": "Exhibition", "turns": 9, "gc": 0, "combos": False, "mld": False, "extra_turns": "nein",
        "desc": "Thema und Idee vor Power. Du zeigst dein Deck her, gewinnen ist Nebensache."},
    2: {"name": "Core", "turns": 8, "gc": 0, "combos": False, "mld": False, "extra_turns": "einzelne ok, kein Chaining",
        "desc": "Unoptimiert, geradlinig, kreativ. Siege kommen schrittweise und sichtbar am Board."},
    3: {"name": "Upgraded", "turns": 6, "gc": 3, "combos": "nicht vor Zug 6", "mld": False, "extra_turns": "kein Chaining",
        "desc": "Starke Synergie und gute Karten. Kann in einem großen Zug gewinnen – aber erst nach Aufbau."},
    4: {"name": "Optimized", "turns": 4, "gc": 99, "combos": True, "mld": True, "extra_turns": "frei",
        "desc": "Tödlich, konsistent, schnell. Alles erlaubt, aber nicht auf das cEDH-Meta gebaut."},
    5: {"name": "cEDH", "turns": 1, "gc": 99, "combos": True, "mld": True, "extra_turns": "frei",
        "desc": "Turnier-Commander: maximal effizient, jede Runde kann die letzte sein."},
}

# Stand 23.11.2026 (Playgroup/Scryfall is:gamechanger). Wird live per Scryfall aktualisiert, das hier ist der Fallback.
GAME_CHANGERS = {
    "Drannith Magistrate", "Enlightened Tutor", "Farewell", "Humility", "Smothering Tithe", "Teferi's Protection",
    "Consecrated Sphinx", "Cyclonic Rift", "Fierce Guardianship", "Force of Will", "Gifts Ungiven", "Intuition",
    "Mystical Tutor", "Narset, Parter of Veils", "Rhystic Study", "Thassa's Oracle",
    "Ad Nauseam", "Bolas's Citadel", "Braids, Cabal Minion", "Demonic Tutor", "Imperial Seal", "Necropotence",
    "Opposition Agent", "Orcish Bowmasters", "Tergrid, God of Fright // Tergrid's Lantern", "Vampiric Tutor",
    "Gamble", "Jeska's Will", "Underworld Breach",
    "Biorhythm", "Crop Rotation", "Natural Order", "Seedborn Muse", "Survival of the Fittest", "Worldly Tutor",
    "Aura Shards", "Coalition Victory", "Grand Arbiter Augustin IV", "Notion Thief",
    "Ancient Tomb", "Chrome Mox", "Field of the Dead", "Gaea's Cradle", "Glacial Chasm", "Grim Monolith",
    "Lion's Eye Diamond", "Mana Vault", "Mishra's Workshop", "Mox Diamond", "Panoptic Mirror", "Serra's Sanctum",
    "The One Ring", "The Tabernacle at Pendrell Vale",
}

# Salt 2026 Top 10 (EDHREC, 16.10.2026)
SALT_TOP = {"Stasis": 3.05, "Armageddon": 2.98, "Winter Orb": 2.93, "The Tabernacle at Pendrell Vale": 2.83,
            "Rhystic Study": 2.82, "Tergrid, God of Fright // Tergrid's Lantern": 2.81, "Grand Arbiter Augustin IV": 2.76,
            "Vivi Ornitier": 2.71, "Static Orb": 2.71, "Ravages of War": 2.63}

# ---------------------------------------------------------------- Glossar
GLOSSARY = {
    "Commander": "Deine legendäre Kreatur in der Kommandozone. Sie bestimmt die Farbidentität und meistens den Plan des Decks.",
    "Farbidentität": "Alle Manasymbole auf dem Commander (auch im Regeltext). Jede Karte im Deck darf nur diese Farben enthalten.",
    "Ramp": "Karten, die dir schneller mehr Mana geben, als nur ein Land pro Zug (z. B. Sol Ring, Cultivate, Llanowar Elves). So spielst du große Sachen früher.",
    "Kartenvorteil": "Karten, die dir mehr Karten bringen (ziehen, aus dem Exil spielen, Discover). Wer keine Karten mehr hat, kann nichts mehr tun.",
    "Removal": "Gezielte Antwort auf eine einzelne Bedrohung: zerstören, exilieren, zurückschicken (z. B. Path to Exile, Beast Within).",
    "Brettwischer": "Board Wipe: entfernt viele oder alle Kreaturen auf einmal (z. B. Wrath of God). Notbremse, wenn jemand davonzieht.",
    "Schutz": "Karten, die deine wichtigen Kreaturen vor Removal oder Brettwischern retten (z. B. Heroic Intervention, Lightning Greaves).",
    "Wincon": "Win Condition: die Karten oder Kombinationen, mit denen du das Spiel tatsächlich gewinnst (z. B. Overrun-Effekt, riesiger Angreifer, Combo).",
    "Synergie": "Karten, die zusammen mehr können als einzeln. Ein Deck mit Synergie hat einen roten Faden.",
    "Value-Engine": "Eine Karte, die immer wieder Vorteil erzeugt, solange sie liegt (z. B. Ripjaw Raptor: jedes Mal Schaden → Karte).",
    "Tutor": "Sucht eine bestimmte Karte aus der Bibliothek. Macht Decks konsistent, aber Spiele auch gleichförmiger.",
    "Game Changer": "Offizielle Liste besonders starker Karten (z. B. Rhystic Study, Demonic Tutor). Bracket 1–2: keine, Bracket 3: maximal 3.",
    "Bracket": "Offizielles Power-Level von 1 (Exhibition) bis 5 (cEDH). Hilft, vor dem Spiel ähnliche Decks zusammenzubringen.",
    "Infinite Combo": "Zwei oder mehr Karten, die zusammen eine Endlosschleife erzeugen (unendlich Mana, Schaden, Token …) und meist sofort gewinnen.",
    "Stax": "Karten, die alle einschränken (z. B. Winter Orb: Länder enttappen nicht). Am Casual-Tisch sehr unbeliebt.",
    "MLD": "Mass Land Destruction: zerstört viele Länder auf einmal (z. B. Armageddon). Erst ab Bracket 4 erlaubt.",
    "Manakurve": "Wie viele Karten du zu welchen Kosten spielst. Ideal: viele 2–3er, wenige teure Karten.",
    "Manawert": "Mana Value (MV): die Gesamtkosten einer Karte. Sol Ring = 1, Pantlaza = 5.",
    "Farbquellen": "Wie viele Länder/Ramp-Karten eine bestimmte Farbe liefern. Für eine Farbe, die du früh brauchst, rund 19.",
    "Fixing": "Länder und Ramp, die mehrere Farben liefern (z. B. Jungle Shrine). Wichtig ab drei Farben.",
    "ETB": "Enters the Battlefield: Effekt, wenn die Karte ins Spiel kommt.",
    "Discover": "Discover X: Decke Karten auf, bis eine Nicht-Land-Karte mit MV ≤ X kommt – die darfst du gratis wirken oder auf die Hand nehmen.",
    "Enrage": "Dinosaurier-Fähigkeit: löst aus, wenn der Kreatur Schaden zugefügt wird.",
    "Goldfish": "Das Deck allein testen: Starthände ziehen und ein paar Züge ohne Gegner spielen.",
    "Mulligan": "Starthand neu ziehen. In Commander ist der erste Mulligan gratis.",
    "Salt": "Wie sehr eine Karte andere Spieler nervt (EDHREC-Umfrage, 0–4).",
    "Rule 0": "Das Gespräch vor dem Spiel: Bracket, Combos, Game Changer ansagen und Erwartungen abgleichen.",
    "Overrun": "Effekt, der alle deine Kreaturen für einen Zug stark macht (z. B. Overrun, Craterhoof). Klassischer Finisher.",
    "Recursion": "Karten aus dem Friedhof zurückholen.",
    "Friedhofshass": "Karten, die gegnerische Friedhöfe leeren (z. B. Bojuka Bog) – Antwort auf Reanimator-Decks.",
    "Turn Mapping": "Für jede Karte überlegen, in welchem Zug du sie realistisch spielst.",
    "Non-Bo": "Zwei Karten in deinem Deck, die sich gegenseitig behindern (z. B. Brettwischer im Kreaturendeck).",
}

# ---------------------------------------------------------------- Archetypen
# fun = Spaß selbst / gegen (1–5, Einschätzung), cx = Komplexität (1–5)
ARCHETYPES = {
    "big-mana": dict(name="Big Mana / Ramp", plan="Früh viel Mana, dann riesige Bedrohungen vor der Zeit.", fun=(5, 3), cx=2,
                     colors="G, Gx", examples=["Pantlaza, Sun-Favored", "Ellie and Alan", "Gishath, Sun's Avatar"], types=["timmy"]),
    "typal": dict(name="Typal (Tribal)", plan="Ein Kreaturentyp plus Lords, die alle stärker machen.", fun=(5, 4), cx=2,
                  colors="je Typ", examples=["The Ur-Dragon", "Gishath, Sun's Avatar", "Edgar Markov"], types=["timmy", "vorthos"]),
    "tokens": dict(name="Tokens / Go-Wide", plan="Board mit Spielsteinen fluten, dann ein großer Angriff.", fun=(4, 3), cx=2,
                   colors="W, G, GW, RW", examples=["Jinnie Fay, Jetmir's Second", "Neyali, Suns' Vanguard"], types=["timmy"]),
    "voltron": dict(name="Voltron", plan="Ausrüstung/Auren auf eine Kreatur, meist den Commander – 21 Commander-Schaden.", fun=(4, 3), cx=2,
                    colors="W, R, WU, RW", examples=["Galea, Kindler of Hope", "Sigarda, Host of Herons"], types=["timmy", "spike"]),
    "aggro": dict(name="Aggro", plan="Früh angreifen, mit Tempo gewinnen.", fun=(4, 3), cx=2,
                  colors="R, W, RW", examples=["Isshin, Two Heavens as One", "Adeline, Resplendent Cathar"], types=["timmy"]),
    "counters": dict(name="+1/+1-Marken", plan="Kreaturen wachsen lassen und vermehren (Proliferate).", fun=(4, 4), cx=3,
                     colors="G, GW, UG", examples=["Hamza, Guardian of Arashin", "Shalai and Hallar"], types=["timmy", "johnny"]),
    "landfall": dict(name="Landfall", plan="Jedes Land löst etwas aus – Ramp ist gleichzeitig Plan.", fun=(4, 4), cx=3,
                     colors="G, GU, Naya", examples=["Tatyova, Benthic Druid", "Omnath, Locus of Rage"], types=["johnny"]),
    "aristocrats": dict(name="Aristocrats", plan="Eigene Kreaturen opfern, jeder Tod lässt die Gegner bluten.", fun=(4, 3), cx=4,
                        colors="B, BW, BR", examples=["Teysa Karlov", "Korvold, Fae-Cursed King"], types=["johnny"]),
    "blink": dict(name="Blink", plan="Kreaturen kurz exilieren und zurückholen, um ETB-Effekte zu wiederholen.", fun=(4, 3), cx=4,
                  colors="W, U, Bant", examples=["Lagrella, the Magpie", "Roon of the Hidden Realm"], types=["johnny"]),
    "spellslinger": dict(name="Spellslinger", plan="Viele Spontanzauber/Hexereien, Payoffs belohnen jeden Spruch.", fun=(4, 3), cx=4,
                         colors="U, R, UR", examples=["Kalamax, the Stormsire", "Veyran, Voice of Duality"], types=["johnny", "melvin"]),
    "artifacts": dict(name="Artefakte", plan="Artefakte und Treasures, Payoffs für jedes Artefakt.", fun=(4, 3), cx=4,
                      colors="U, R, farblos", examples=["Urtet, Remnant of Memnarch", "Cid, Timeless Artificer"], types=["johnny"]),
    "enchantress": dict(name="Enchantress", plan="Verzauberungen spielen und dafür Karten ziehen.", fun=(4, 3), cx=3,
                        colors="GW", examples=["Anikthea, Hand of Erebos", "Sythis, Harvest's Hand"], types=["johnny"]),
    "reanimator": dict(name="Reanimator", plan="Friedhof füllen, die größten Kreaturen billig zurückholen.", fun=(4, 3), cx=4,
                       colors="B, BG, UB", examples=["Meren of Clan Nel Toth", "Kagha, Shadow Archdruid"], types=["timmy", "johnny"]),
    "cascade": dict(name="Cascade / Discover", plan="Gratis-Zauber durch Kaskade/Discover – viel Wert, viel Überraschung.", fun=(4, 3), cx=3,
                    colors="Temur, Jund, Naya", examples=["Pantlaza, Sun-Favored", "Maelstrom Wanderer", "Yidris, Maelstrom Wielder"], types=["timmy", "chaos"]),
    "chaos": dict(name="Chaos", plan="Unvorhersehbarkeit maximieren: Münzwürfe, Tauschen, Warp World.", fun=(5, 3), cx=3,
                  colors="UR, R", examples=["Okaun, Eye of Chaos & Zndrsplt", "Yusri, Fortune's Flame", "Karona, False God"], types=["chaos"]),
    "politics": dict(name="Politik / Goad / Monarch", plan="Gegner gegeneinander lenken, Deals machen.", fun=(4, 4), cx=4,
                     colors="R, U, Jeskai, Mardu", examples=["Nelly Borca, Impulsive Accuser", "Firkraag, Cunning Instigator"], types=["johnny"]),
    "group-hug": dict(name="Group Hug", plan="Allen helfen, damit dich niemand angreift – und heimlich gewinnen.", fun=(3, 5), cx=3,
                      colors="GU, Bant", examples=["Kynaios and Tiro of Meletis", "Phelddagrif"], types=["vorthos"]),
    "lifegain": dict(name="Lifegain", plan="Leben gewinnen und in Schaden oder Karten verwandeln.", fun=(4, 3), cx=2,
                     colors="W, WB", examples=["Oloro, Ageless Ascetic", "Liesa, Shroud of Dusk"], types=["timmy"]),
    "wheels": dict(name="Wheels", plan="Alle werfen ihre Hand ab und ziehen neu – Payoffs bestrafen das.", fun=(4, 3), cx=3,
                   colors="UR, BR", examples=["Nekusar, the Mindrazer", "Xyris, the Writhing Storm"], types=["chaos", "johnny"]),
    "control": dict(name="Control", plan="Überleben, Bedrohungen beseitigen, spät gewinnen.", fun=(3, 2), cx=4,
                    colors="U, UB, UW", examples=["Y'shtola, Night's Blessed", "Talrand, Sky Summoner"], types=["spike"]),
    "combo": dict(name="Combo", plan="Bestimmte Karten zusammenbringen und sofort gewinnen.", fun=(3, 2), cx=5,
                  colors="alle, oft U/B", examples=["Kinnan, Bonder Prodigy", "Thrasios + Tymna"], types=["spike", "johnny"]),
}

# ---------------------------------------------------------------- Fragebogen
# Jede Antwort gibt Punkte auf Archetypen. Beispiele helfen beim Antworten.
QUESTIONNAIRE = [
    {"id": "moment", "q": "Welcher Moment in einem Spiel macht dich am glücklichsten?", "options": [
        {"id": "a", "t": "Ein riesiges Monster auf den Tisch knallen", "ex": "Zacama für 9 Mana, Etali deckt drei Zauber auf", "pts": {"big-mana": 3, "typal": 2, "reanimator": 1}},
        {"id": "b", "t": "Wenn meine Engine läuft und alles ineinandergreift", "ex": "Jeder Tod zieht eine Karte und macht Schaden", "pts": {"aristocrats": 3, "blink": 2, "artifacts": 2, "spellslinger": 2}},
        {"id": "c", "t": "Wenn keiner weiß, was als Nächstes passiert", "ex": "Discover 10 deckt etwas Absurdes auf", "pts": {"chaos": 3, "cascade": 3, "wheels": 1}},
        {"id": "d", "t": "Gewinnen, egal wie", "ex": "Zug 6: Combo, fertig", "pts": {"combo": 3, "control": 2}},
        {"id": "e", "t": "Wenn mein Deck eine Geschichte erzählt", "ex": "Final-Fantasy-Party mit allen Helden", "pts": {"typal": 2, "group-hug": 1, "politics": 1}},
    ]},
    {"id": "table", "q": "Wie willst du mit den anderen am Tisch umgehen?", "options": [
        {"id": "a", "t": "Alle angreifen, jede Runde", "ex": "Mit 20 Token in alle Richtungen", "pts": {"aggro": 3, "tokens": 2, "voltron": 2}},
        {"id": "b", "t": "Deals machen, andere gegeneinander lenken", "ex": "„Greif lieber ihn an, er hat den Drachen“", "pts": {"politics": 3, "group-hug": 1}},
        {"id": "c", "t": "Allen etwas geben, damit mich keiner angreift", "ex": "Jeder zieht eine Extra-Karte", "pts": {"group-hug": 3}},
        {"id": "d", "t": "In Ruhe aufbauen und dann zuschlagen", "ex": "Erst Ramp, dann ab Zug 6 die großen Dinos", "pts": {"big-mana": 2, "landfall": 2, "enchantress": 2, "control": 1}},
    ]},
    {"id": "chaos", "q": "Wie viel Glück und Zufall magst du?", "options": [
        {"id": "a", "t": "Je verrückter, desto besser", "ex": "Münzwürfe, Warp World, Kaskaden-Ketten", "pts": {"chaos": 3, "cascade": 3, "wheels": 2}},
        {"id": "b", "t": "Etwas Varianz ist gut", "ex": "Discover und Kartenziehen, aber mit klarem Plan", "pts": {"cascade": 1, "big-mana": 1, "tokens": 1, "counters": 1}},
        {"id": "c", "t": "Ich will die Kontrolle", "ex": "Ich suche mir genau die Karte, die ich brauche", "pts": {"control": 2, "combo": 2}},
    ]},
    {"id": "complexity", "q": "Wie komplex dürfen deine Züge sein?", "options": [
        {"id": "a", "t": "Einfach: Karte spielen, angreifen", "ex": "Dino raus, draufhauen", "pts": {"aggro": 2, "voltron": 2, "typal": 2, "tokens": 2, "big-mana": 2}},
        {"id": "b", "t": "Ein paar Trigger sind ok", "ex": "Landfall-Auslöser, Marken verteilen", "pts": {"counters": 2, "landfall": 2, "lifegain": 2, "cascade": 1}},
        {"id": "c", "t": "Gerne viele Trigger und Entscheidungen", "ex": "Opfern, Blink, Stapel-Tricks", "pts": {"aristocrats": 2, "spellslinger": 2, "blink": 2, "wheels": 2, "combo": 1}},
    ]},
    {"id": "finish", "q": "Wie soll das Spiel enden?", "options": [
        {"id": "a", "t": "Mit Kampf und Commander-Schaden", "ex": "Pantlaza mit Rüstung trifft 21-mal", "pts": {"voltron": 3, "aggro": 2}},
        {"id": "b", "t": "Ein riesiger Angriff mit vielen Kreaturen", "ex": "Overrun mit 12 Dinos", "pts": {"tokens": 3, "typal": 3, "big-mana": 1}},
        {"id": "c", "t": "Alle verlieren gleichzeitig Leben", "ex": "Jeder Tod: alle Gegner −1", "pts": {"aristocrats": 3, "lifegain": 2}},
        {"id": "d", "t": "Eine clevere Combo", "ex": "Zwei Karten, unendlich Schaden", "pts": {"combo": 3, "artifacts": 1, "blink": 1}},
        {"id": "e", "t": "Irgendwie absurd", "ex": "Die Gegner tauschen alles und verlieren daran", "pts": {"chaos": 3, "wheels": 2}},
    ]},
    {"id": "bad", "q": "Was ist für dich ein schlechtes Spiel?", "options": [
        {"id": "a", "t": "Wenn ich nichts machen darf", "ex": "Stax, Länder zerstört", "pts": {}},
        {"id": "b", "t": "Wenn es vor Zug 6 vorbei ist", "ex": "Plötzlich-Combo in Zug 4", "pts": {"combo": -3}},
        {"id": "c", "t": "Wenn es ewig dauert", "ex": "Drei Brettwischer, 3 Stunden", "pts": {"control": -2, "group-hug": -1}},
        {"id": "d", "t": "Wenn ich chancenlos verliere", "ex": "Ein Spieler zieht weg und keiner kann was tun", "pts": {"control": 1}},
    ]},
]


def score_questionnaire(answers: dict) -> list[dict]:
    """answers: {frage_id: [option_ids]} → Top-Archetypen mit Begründung."""
    scores = {k: 0 for k in ARCHETYPES}
    reasons = {k: [] for k in ARCHETYPES}
    for q in QUESTIONNAIRE:
        for oid in answers.get(q["id"], []):
            opt = next((o for o in q["options"] if o["id"] == oid), None)
            if not opt:
                continue
            for k, p in opt["pts"].items():
                scores[k] += p
                if p > 0:
                    reasons[k].append(opt["t"])
    ranked = sorted(scores.items(), key=lambda kv: -kv[1])
    out = []
    for k, s in ranked[:5]:
        if s <= 0:
            continue
        a = ARCHETYPES[k]
        out.append({"id": k, "score": s, **a, "why": reasons[k][:3]})
    return out


# ---------------------------------------------------------------- Assistent-Schritte
STEPS = [
    {"id": "table", "title": "Tisch & Bracket", "role": None,
     "lesson": "Bevor du eine Karte auswählst, klärst du, gegen wen du spielst. Ein Deck, das deinen Tisch überrollt, macht genauso wenig Spaß wie eines, das nie mithält. Das Bracket ist euer gemeinsamer Maßstab.",
     "questions": ["Wie stark sind die Decks deiner Mitspieler? (z. B. „Precons mit ein paar Upgrades“)",
                   "Wie lange sollen Spiele dauern? (z. B. „1–2 Stunden, mindestens 8 Züge“)",
                   "Was soll in diesem Deck tabu sein? (z. B. „keine Infinite-Combos vor Zug 8“)"]},
    {"id": "commander", "title": "Commander", "role": None,
     "lesson": "Der Commander bestimmt deine Farben und meistens den Plan. Drei Wege zum Commander: von einer Strategie aus („Ich will Dinos“), von einer Figur aus („Ich liebe Cloud“) oder von deiner Sammlung aus.",
     "questions": ["Was reizt dich an diesem Commander? (z. B. „Discover ist herrlich chaotisch“)",
                   "Was macht er jede Runde, wenn er liegt?"]},
    {"id": "plan", "title": "Spielplan in einem Satz", "role": None,
     "lesson": "Profis schreiben zuerst auf, wie das Deck gewinnt – in einem Satz. Jede spätere Karte muss sich daran messen lassen: Bringt sie mich diesem Satz näher?",
     "questions": ["Wie gewinnst du? Beispiel: „Ich rampe früh, spiele große Dinos, die über Discover Gratis-Zauber bringen, und gewinne mit einem Angriff.“",
                   "Welcher Moment soll sich großartig anfühlen?"]},
    {"id": "wincon", "title": "Wincons", "role": "wincon",
     "lesson": "Wincons sind die Karten, die ein gutes Board in einen Sieg verwandeln. EDHREC empfiehlt mindestens 7, damit du sie auch ziehst. Combos zählen auch – achte dann auf das Bracket.",
     "questions": ["Welche Karte beendet das Spiel, wenn dein Plan aufgeht?"]},
    {"id": "synergy", "title": "Thema & Synergie", "role": "synergy",
     "lesson": "Das Herz des Decks: 25–35 Karten, die deinen Plan tragen. Lieber 8 Karten, die zusammenarbeiten, als 8 starke Einzelkarten ohne roten Faden.",
     "questions": ["Welche Mechanik soll tragen? (z. B. „Enrage“, „Discover“, „Token“)"]},
    {"id": "ramp", "title": "Ramp", "role": "ramp",
     "lesson": "Ramp bringt dich schneller an deine starken Karten. Teurer Commander (5+) → mindestens 10. Achte auf die Art: Land-Ramp (Farseek) fixt gleich deine Farben, Rocks (Arcane Signet) sind schnell.",
     "questions": ["Wie teuer ist dein Commander und wann willst du ihn spielen?"]},
    {"id": "draw", "title": "Kartenvorteil", "role": "draw",
     "lesson": "Ohne Karten auf der Hand ist jedes Deck tot. Wiederholbare Engines (jede Runde eine Karte) sind meist besser als einmaliges Ziehen. Discover und Kaskade zählen hier mit.",
     "questions": ["Willst du lieber Engines oder einmalige Draw-Zauber?"]},
    {"id": "removal", "title": "Interaktion", "role": "removal",
     "lesson": "Du brauchst Antworten auf gegnerische Bedrohungen: 8–12 gezielte Antworten, davon ein paar gegen Artefakte/Verzauberungen. Billig und flexibel ist Trumpf (z. B. Beast Within, Generous Gift).",
     "questions": ["Was macht dir an anderen Decks Probleme? (z. B. „fliegende Drachen“, „Artefakt-Engines“)"]},
    {"id": "wipe", "title": "Brettwischer", "role": "wipe",
     "lesson": "2–4 Notbremsen, falls jemand davonzieht. Vorsicht im eigenen Kreaturendeck (Non-Bo!) – einseitige Wischer oder solche, die deine großen Kreaturen überleben, passen besser.",
     "questions": ["Würdest du dein eigenes Board opfern, um ein gegnerisches zu stoppen?"]},
    {"id": "protection", "title": "Schutz", "role": "protection",
     "lesson": "Wenn dein Commander der Plan ist oder du viel auf ein Board setzt, brauchst du Schutz (Heroic Intervention, Lightning Greaves). 2–6 Karten.",
     "questions": ["Was passiert mit deinem Plan, wenn ein Brettwischer kommt?"]},
    {"id": "lands", "title": "Länder & Manabasis", "role": "land",
     "lesson": "Faustregel (Burgess): 31 + Anzahl Farben + Manawert des Commanders. Bei drei Farben brauchst du Fixing: Duals, Tri-Lands, Command Tower. Höchstens ~4 getappte Länder.",
     "questions": ["Welche Farbe brauchst du am frühesten?"]},
    {"id": "curve", "title": "Kurve & Kürzen", "role": None,
     "lesson": "Zähl durch: Ø-Manawert um 3, wenige Karten über 7. Zum Kürzen „von oben“: teure, langsame Karten zuerst. Eins-zu-eins tauschen, damit du dich nicht verzählst.",
     "questions": ["Welche Karte tut am wenigsten für deinen Spielplan?"]},
    {"id": "check", "title": "Bracket-, Combo- & Spaß-Check", "role": None,
     "lesson": "Ehrliche Einstufung: Game Changer zählen, Combos prüfen, deine No-Gos (Stax, Landzerstörung, lange Züge) checken. Danach weißt du, was du am Tisch ansagen solltest.",
     "questions": ["Gibt es Karten, die du vor dem Spiel ansagen solltest?"]},
    {"id": "rule0", "title": "Rule-0-Spickzettel", "role": None,
     "lesson": "Fertig! Dein Spickzettel fürs Gespräch vor dem Spiel: Bracket, Plan in einem Satz, Game Changer, Combos.",
     "questions": []},
]

STEP_IDS = [s["id"] for s in STEPS]

# Scryfall-Suchen pro Rolle (Oracle-Text-Fallbacks, weil nicht alle Tagger-Namen verifiziert sind)
ROLE_QUERIES = {
    "ramp": "(otag:ramp)",
    "draw": "(otag:card-advantage)",
    "removal": "(otag:removal -o:\"all creatures\" -o:\"each creature\")",
    "wipe": "(o:\"destroy all\" or o:\"exile all\" or o:\"damage to each creature\" or o:\"all creatures get -\")",
    "protection": "((o:indestructible or o:hexproof or o:\"phase out\") (o:\"creatures you control\" or o:\"permanents you control\" or o:\"equipped creature\"))",
    "wincon": "((o:\"creatures you control get +\" o:trample) or o:\"double strike\" or o:\"each opponent loses\" or o:\"win the game\")",
    "land": "t:land -t:basic",
    "synergy": "",
}

# EDHREC-Listenüberschriften → Rolle
EDHREC_HEADERS = {
    "ramp": ["Mana Artifacts", "Ramp"],
    "draw": ["Card Draw", "Card Advantage"],
    "removal": ["Removal", "Interaction"],
    "wipe": ["Board Wipes", "Boardwipes", "Wipes"],
    "protection": ["Protection"],
    "land": ["Lands", "Utility Lands"],
    "synergy": ["High Synergy Cards", "Top Cards", "Creatures", "New Cards"],
    "wincon": ["High Synergy Cards", "Top Cards"],
}

# ---------------------------------------------------------------- No-Go-Erkennung
import re as _re

NOGO_PATTERNS = {
    "stax": [r"don't untap", r"doesn't untap", r"can't untap", r"players can't cast", r"can't cast more than",
             r"spells cost \{\d\} more", r"each player can't", r"skip (their|your) untap", r"players can't search"],
    "mld": [r"destroy all lands", r"each player sacrifices (all|\w+) lands", r"exile all lands", r"lands don't untap",
            r"nonbasic lands are mountains"],
    "long_turns": [r"take an extra turn", r"copy it for each", r"for each (creature|permanent) you control, create"],
}


def nogo_flags(card: dict) -> list[str]:
    t = (card.get("oracle_text") or "").lower()
    out = []
    for key, pats in NOGO_PATTERNS.items():
        if any(_re.search(p, t) for p in pats):
            out.append(key)
    return out


NOGO_LABELS = {"stax": "Stax/Lock", "mld": "Massen-Landzerstörung", "long_turns": "lange Züge", "combos_early": "frühe Infinites"}

DEFAULT_PROFILE = {
    "coach_style": "teacher",           # Lehrer: ich entscheide
    "fun": ["timmy", "johnny", "chaos"],  # große Momente, clevere Kombis, Chaos & Zufall
    "table": "mixed",
    "knowledge": "beginner",            # ganz von vorn → alles erklären
    "combos": "suggest",                # aktiv vorschlagen
    "nogos": ["long_turns", "stax", "mld"],
    "questionnaire": {},
}
