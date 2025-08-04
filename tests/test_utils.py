from utils import reformat_currency

def test_utils():
    assert reformat_currency("Chaos Orb", 12.341) == "Chaos Orb: 12.34c"