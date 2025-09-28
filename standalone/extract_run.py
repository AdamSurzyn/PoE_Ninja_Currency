from dotenv import load_dotenv

from src.db_inserts.bq_dim_merge import run_poe_merge
from src.fetcher import get_poe_data
from src.db_inserts.bq_insert_stg import db_insert_currency
from src.db_inserts.bq_dim_merge import run_poe_fact_merge
from src.utilities import reformat_all_data
from src.logger import setup_logger

BASE_URL = 'https://poe.ninja/api/data/currencyoverview'
MERCENERIES_PARAMS = {
    'league': 'Mercenaries',
    'type': 'Currency'
}
SOURCE = "PoE Ninja API"

def run():
    setup_logger()
    load_dotenv()

    league = MERCENERIES_PARAMS["league"]
    
    data = get_poe_data(BASE_URL, MERCENERIES_PARAMS)

    if not data or "lines" not in data or not data["lines"]:
        print("No data!")
        return
    
    results = data["lines"]
    reformatted = reformat_all_data(results, SOURCE, league)

    print(reformatted[0])
    db_insert_currency(reformatted, "currency_rates_stg")
    run_poe_fact_merge("src/sql/merge_currency_fact.sql")
    run_poe_merge("src/sql/merge_currency_dim.sql")
    run_poe_merge("src/sql/merge_currency_league.sql")
    run_poe_merge("src/sql/merge_currency_currencies.sql")
    run_poe_merge("src/sql/merge_currency_sources.sql")
    return 1

if __name__ == "__main__":
    run()