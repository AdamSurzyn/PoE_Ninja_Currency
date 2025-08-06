from dags.python_scripts.fetcher import get_poe_data
import pytest


def test_get_poe_data_raises_on_missing_url():
    with pytest.raises(ValueError):
        get_poe_data("", {"type": "Currency"})

def test_get_poe_data_returns_json(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return{"lines": [{"currencyTypeName": "Chaos Orb", "value": 1.0}]}
        
    def fake_get(url, params, timeout):
        return FakeResponse()
    
    monkeypatch.setattr("requests.get", fake_get)

    result = get_poe_data("fake-url", {"type": "Currency"})
    
    assert "lines" in result
    assert result["lines"][0]["currencyTypeName"] == "Chaos Orb"