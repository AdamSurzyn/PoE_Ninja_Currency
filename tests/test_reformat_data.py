from src.utilities import reformat_all_data
import datetime
def test_reformat_all_data():

    sample_input = [
        {
            "currencyTypeName": "Exalted Orb",
            "receive": {
                "sample_time_utc": "2025-08-04T16:15:32Z",
                "count": 50,
                "value": 150.5
            },
            "detailsId": "exalted"
        }
    ]
    source = "test_source"
    league = "test_league"
    result = reformat_all_data(sample_input, source, league)
    assert isinstance(result, list)

    assert len(result) == 1

    item = result[0]

    assert item["currency_type_name"] == "Exalted Orb"
    assert item["sample_time_utc"] == datetime.datetime(2025, 8, 4, 16, 0)
    assert item["count"] == 50
    assert item["value_chaos"] == 150.5
    assert item["detailsid"] == "exalted"
    assert item["source"] == source
    assert item["league"] == league

