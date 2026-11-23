from app import analysis, collectr


def test_candidates():
    assert collectr.candidates("Paradise Chocobo - Birds of Paradise (Borderless)")[0] == "Birds of Paradise"
    assert collectr.candidates("Sol Ring (0356)") == ["Sol Ring"]
    assert collectr.candidates("Sphere Grid (Extended Art)") == ["Sphere Grid"]


def test_parse_collectr():
    csv = ("Portfolio Name,Category,Set,Product Name,Card Number,Rarity,Variance,Grade,Card Condition,Average Cost Paid,Quantity,Market Price (As of 2026-10-11),Price Override,Watchlist,Date Added,Notes\n"
           ",Pokemon,X,Pikachu,1,R,,,,,1,2,0,false,,\n"
           ",Magic: The Gathering,Ixalan,Raging Swordtooth,1,R,Normal,,,,2,1.64,0,false,,\n"
           ",Magic: The Gathering,AFR,Dungeon of the Mad Mage // Goblin Double-sided Token,1,T,Normal,,,,1,0.3,0,false,,\n")
    rows = collectr.parse(csv)
    assert len(rows) == 1 and rows[0]["qty"] == 2 and rows[0]["price_usd"] == 1.64


def test_decklist():
    l = collectr.parse_decklist("Commander\n1 Pantlaza, Sun-Favored\nDeck\n1x Sol Ring\n8 Forest\nCultivate (LCC) 12 *F*")
    assert l[0] == {"name": "Pantlaza, Sun-Favored", "qty": 1, "section": "commander"}
    assert l[-1]["name"] == "Cultivate" and l[2]["qty"] == 8


def test_categories():
    assert "ramp" in analysis.categories({"type_line": "Artifact", "oracle_text": "{T}: Add {C}{C}."})
    assert "removal" in analysis.categories({"type_line": "Instant", "oracle_text": "Exile target creature."})
    assert "wipe" in analysis.categories({"type_line": "Sorcery", "oracle_text": "Destroy all creatures."})
    assert "draw" in analysis.categories({"type_line": "Creature", "oracle_text": "you may discover X"})
    assert analysis.categories({"type_line": "Basic Land — Forest", "oracle_text": ""}) == ["land"]
    assert "protection" in analysis.categories({"type_line": "Creature", "oracle_text": "Sacrifice it: Creatures you control gain indestructible until end of turn."})


def test_bracket():
    assert analysis.estimate_bracket([], [])[0] == 2
    assert analysis.estimate_bracket(["Rhystic Study"], [])[0] == 3
    assert analysis.estimate_bracket(["a", "b", "c", "d"], [])[0] == 4
