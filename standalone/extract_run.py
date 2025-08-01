from dags.python_scripts.fetcher import get_poe_data
from dags.python_scripts.db_inserts.db_insert_stg import db_insert_currency
from dags.python_scripts.logger import setup_logger
from dags.python_scripts.utilities import reformat_all_data


BASE_URL = 'https://poe.ninja/api/data/currencyoverview'
MERCANERIES_PARAMS = {
    'league': 'Mercenaries',
    'type': 'Currency'
}
SOURCE = "PoE Ninja API"

def run():
    league = MERCANERIES_PARAMS["league"]
    try:
        setup_logger()
        data = get_poe_data(BASE_URL, MERCANERIES_PARAMS)
        if not data:
            print("No data!")
            return
        results = data["lines"]
        reformatted = reformat_all_data(results, SOURCE, league)
        print(reformatted[0])
        db_insert_currency(reformatted)
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    run()