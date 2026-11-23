from app import knowledge as K


def test_questionnaire_scoring():
    top = K.score_questionnaire({"moment": ["a", "c"], "chaos": ["a"]})
    ids = [t["id"] for t in top]
    assert "cascade" in ids[:3] and "big-mana" in ids


def test_adjusted_targets():
    t = K.adjusted_targets(5, "big-mana", 3)
    assert t["ramp"][1] == 15
    assert t["lands"][1] <= 39 <= t["lands"][2]  # Burgess: 31 + 3 + 5


def test_nogo_flags():
    assert "stax" in K.nogo_flags({"oracle_text": "Players can't cast more than one spell each turn."})
    assert "mld" in K.nogo_flags({"oracle_text": "Destroy all lands."})
    assert K.nogo_flags({"oracle_text": "Draw a card."}) == []


def test_steps_and_glossary():
    assert K.STEP_IDS[0] == "table" and "rule0" in K.STEP_IDS
    assert "Ramp" in K.GLOSSARY and len(K.GAME_CHANGERS) >= 50
