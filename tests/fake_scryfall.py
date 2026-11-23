"""Mini-Scryfall für lokale Tests (echtes Scryfall ist aus der Testumgebung nicht erreichbar).
Liefert für jeden Namen eine plausible Karte; ein paar bekannte Karten haben echte Werte."""
from fastapi import FastAPI, Request

app = FastAPI()
KNOWN = {
    "pantlaza, sun-favored": dict(type_line="Legendary Creature — Dinosaur", mana_cost="{2}{R}{G}{W}", cmc=5, color_identity=["G", "R", "W"], toughness="4",
        oracle_text="Whenever Pantlaza or another Dinosaur you control enters, you may discover X, where X is that creature's toughness."),
    "sol ring": dict(type_line="Artifact", mana_cost="{1}", cmc=1, color_identity=[], oracle_text="{T}: Add {C}{C}.", game_changer=False),
    "cultivate": dict(type_line="Sorcery", mana_cost="{2}{G}", cmc=3, color_identity=["G"], oracle_text="Search your library for up to two basic land cards..."),
    "path to exile": dict(type_line="Instant", mana_cost="{W}", cmc=1, color_identity=["W"], oracle_text="Exile target creature."),
    "rhystic study": dict(type_line="Enchantment", mana_cost="{2}{U}", cmc=3, color_identity=["U"], oracle_text="Whenever an opponent casts a spell, you may draw a card unless...", game_changer=True),
    "forest": dict(type_line="Basic Land — Forest", cmc=0, color_identity=["G"], produced_mana=["G"], oracle_text="({T}: Add {G}.)"),
    "mountain": dict(type_line="Basic Land — Mountain", cmc=0, color_identity=["R"], produced_mana=["R"], oracle_text="({T}: Add {R}.)"),
    "plains": dict(type_line="Basic Land — Plains", cmc=0, color_identity=["W"], produced_mana=["W"], oracle_text="({T}: Add {W}.)"),
    "polyraptor": dict(type_line="Creature — Dinosaur", mana_cost="{6}{G}{G}", cmc=8, color_identity=["G"], toughness="5", oracle_text="Enrage — Whenever Polyraptor is dealt damage, create a token that's a copy of Polyraptor."),
    "selfless spirit": dict(type_line="Creature — Spirit", mana_cost="{1}{W}", cmc=2, color_identity=["W"], oracle_text="Flying. Sacrifice Selfless Spirit: Creatures you control gain indestructible until end of turn."),
}
P = "Partner (You can have two commanders if both have partner.)"
KNOWN.update({
    "thrasios, triton hero": dict(type_line="Legendary Creature — Merfolk Wizard", mana_cost="{G}{U}", cmc=2, color_identity=["G", "U"], oracle_text="{4}: Scry 1, then reveal the top card of your library.\n" + P),
    "tymna the weaver": dict(type_line="Legendary Creature — Human Cleric", mana_cost="{1}{W}{B}", cmc=3, color_identity=["W", "B"], oracle_text="Lifelink\n" + P),
    "kraum, ludevic's opus": dict(type_line="Legendary Creature — Zombie Horror", mana_cost="{3}{U}{R}", cmc=5, color_identity=["U", "R"], oracle_text="Flying, haste\n" + P),
    "wilson, refined grizzly": dict(type_line="Legendary Creature — Bear Warrior", mana_cost="{1}{G}", cmc=2, color_identity=["G"], oracle_text="Reach, trample, ward {2}\nChoose a Background (You can have a Background as a second commander.)"),
    "raised by giants": dict(type_line="Legendary Enchantment — Background", mana_cost="{5}{G}", cmc=6, color_identity=["G"], oracle_text="Commander creatures you own have base power and toughness 10/10 and are Giants in addition to their other types."),
})
BAD = {"paradise chocobo", "castle dracula"}


def card(name):
    k = name.lower()
    base = KNOWN.get(k)
    if base is None:
        land = any(w in k for w in ["glade", "vista", "retreat", "tower", "wilds", "orchard", "village", "snarl", "trail", "shrine", "run", "bridge", "landscape", "ancestry", "passage", "courtyard", "temple", "expanse", "thriving", "territory", "arch of", "garden"])
        base = dict(type_line="Land" if land else "Creature — Dinosaur", mana_cost="" if land else "{3}{G}", cmc=0 if land else (len(name) % 7) + 1,
                    color_identity=[] if land else ["G"], produced_mana=["G", "R", "W"] if land else [], toughness="5", oracle_text="Trample")
    return {"object": "card", "name": name.title() if k not in KNOWN else name, "legalities": {"commander": "legal"},
            "prices": {"eur": "0.50", "usd": "0.60"}, "purchase_uris": {"cardmarket": "https://www.cardmarket.com/x"},
            "image_uris": {"normal": "", "small": ""}, **base}


@app.post("/cards/collection")
async def collection(req: Request):
    ids = (await req.json())["identifiers"]
    data, nf = [], []
    for i in ids:
        (nf if i["name"].lower() in BAD else data).append(i if i["name"].lower() in BAD else card(i["name"]))
    return {"data": data, "not_found": nf}


@app.get("/cards/named")
def named(fuzzy: str):
    if fuzzy.lower() in BAD:
        from fastapi import HTTPException
        raise HTTPException(404)
    return card(fuzzy)


@app.get("/cards/autocomplete")
def ac(q: str):
    return {"data": [n for n in KNOWN if q.lower() in n][:10]}


@app.get("/cards/search")
def search(q: str, order: str = "", unique: str = ""):
    if "gamechanger" in q:
        return {"data": [card("Rhystic Study")] + [card(f"Gc Card {i}") for i in range(25)]}
    if "if both have partner" in q:
        return {"data": [card(n) for n in ["Thrasios, Triton Hero", "Tymna the Weaver", "Kraum, Ludevic's Opus"]]}
    if "t:background" in q:
        return {"data": [card("Raised by Giants")]}
    names = ["Sol Ring", "Cultivate", "Path to Exile", "Selfless Spirit", "Polyraptor", "Heroic Intervention", "Kodama's Reach"]
    return {"data": [card(n) for n in names]}
