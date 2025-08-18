import logging
from python_scripts.fetcher import get_poe_data
from python_scripts.db_inserts.db_insert_stg import db_insert_currency
from python_scripts.logger import setup_logger
from python_scripts.utilities import reformat_all_data, save_csv_results

BASE_URL = 'https://poe.ninja/api/data/currencyoverview'
MERCANERIES_PARAMS = {
    'league': 'Mercenaries',
    'type': 'Currency'  
}
SOURCE = "PoE Ninja API" #Adding source here, will move it once I have more sources
def get_data():
    league = MERCANERIES_PARAMS["league"]
    try:
        setup_logger()
        data = get_poe_data(BASE_URL, MERCANERIES_PARAMS)
        if not data:
            logging.error("Data not received")
            return
        results = data["lines"]
        #save_csv_results(results)
        reformatted = reformat_all_data(results, SOURCE, league)
        print(reformatted)
        db_insert_currency(reformatted)
    except Exception as e:
        print(f"Error in main: {e}")
    
if __name__ == "__main__":
    get_data()