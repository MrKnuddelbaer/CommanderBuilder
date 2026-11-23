from app import knowledge as K

P = "Partner (You can have two commanders if both have partner.)"


def c(name, text, tl="Legendary Creature"):
    return {"name": name, "oracle_text": text, "type_line": tl}


def test_pairs():
    assert K.pair_check(c("A", P), c("B", "Lifelink\n" + P))[0]
    assert K.pair_check(c("Wilson", "Choose a Background (...)"), c("Raised by Giants", "...", "Legendary Enchantment — Background"))[0]
    assert K.pair_check(c("Pir", "Partner with Toothy (...)"), c("Toothy", "Partner with Pir (...)"))[0]
    assert not K.pair_check(c("Pir", "Partner with Toothy (...)"), c("X", P))[0]
    assert not K.pair_check(c("A", P), c("Wilson", "Choose a Background (...)"))[0]
    assert K.pair_check(c("Doc", "...", "Legendary Creature — Time Lord Doctor"), c("Rose", "Doctor's companion (...)"))[0]
    assert K.partner_query(c("Wilson", "Choose a Background")) == "t:background"
