import datetime
import dags.python_scripts.db_inserts.db_insert_stg as mod
from unittest.mock import MagicMock

def test_happy_path_executes_insert(monkeypatch):
    fake_conn = MagicMock()
    fake_cm = MagicMock()

    fake_cm.__enter__.return_value = fake_conn
    fake_cm.__exit__.return_value = False

    fake_engine = MagicMock()
    fake_engine.begin.return_value = fake_cm
    monkeypatch.setattr(
        mod, 
        "get_sqlalchemy_engine", 
        lambda: fake_engine
    )
    
    monkeypatch.setattr(
        mod,
        "Table",
        lambda *a, **k: MagicMock()
    )

    monkeypatch.setattr(
        mod,
        "insert",
        lambda table: MagicMock()
    )

    payload = {
    "currency_type_name": "Chaos Orb",
    "sample_time_utc": datetime.datetime(2025, 8, 4, 16, 0),
    "count": 100,
    "value_chaos": 1.0,
    "detailsid": "chaos",
    "source": "ninja_api",
    "league": "Settlers"
    }

    mod.db_insert_currency(payload)

    fake_engine.begin.assert_called_once()
    fake_conn.execute.assert_called_once()