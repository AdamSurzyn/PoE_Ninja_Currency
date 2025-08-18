from src.fetcher import get_poe_data
from src.db_inserts.db_insert_stg import db_insert_currency
from src.db_inserts.db_insert_dim import db_insert_currency_dim
from src.db_inserts.db_insert_cur import db_insert_currency_data 
from src.logger import setup_logger
from src.utilities import reformat_all_data, get_sqlalchemy_engine
from src.lock import acquire_job_lock, release_job_lock
from dotenv import load_dotenv

BASE_URL = 'https://poe.ninja/api/data/currencyoverview'
MERCANERIES_PARAMS = {
    'league': 'Mercenaries',
    'type': 'Currency'
}
SOURCE = "PoE Ninja API"

def run():
    load_dotenv()
    league = MERCANERIES_PARAMS["league"]
    engine = get_sqlalchemy_engine()
    lock_conn = acquire_job_lock(engine)
    if lock_conn is None:
        print("Another run is active; exiting without doing work.")
        return 0
    try:
        setup_logger()
        data = get_poe_data(BASE_URL, MERCANERIES_PARAMS)
        if not data or "lines" not in data or not data["lines"]:
            print("No data!")
            return 0
        results = data["lines"]
        reformatted = reformat_all_data(results, SOURCE, league)
        print(reformatted[0])
        db_insert_currency(reformatted)
        db_insert_currency_dim()
        db_insert_currency_data()
        return 1
    except Exception as e:
        print(f"ERROR: {e}")
        return 0
    finally:
        release_job_lock(lock_conn)

if __name__ == "__main__":
    run()