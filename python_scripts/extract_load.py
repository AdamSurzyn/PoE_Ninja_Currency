import logging
from python_scripts.fetcher import get_poe_data
from python_scripts.db_inserts.db_insert_stg import db_insert_currency
from python_scripts.logger import setup_logger
from python_scripts.utilities import reformat_all_data, save_csv_results

BASE_URL = 'https://poe.ninja/api/data/currencyoverview'
SETTLERS_PARAMS = {
    'league': 'Settlers',
    'type': 'Currency'  
}
SOURCE = "PoE Ninja API" #Adding source here, will move it once I have more sources
def get_data():
    try:
        setup_logger()
        data = get_poe_data(BASE_URL, SETTLERS_PARAMS)
        if not data:
            logging.error("Data not received")
            return

        results = data["lines"]
        save_csv_results(results)

        reformatted = reformat_all_data(results, SOURCE)
        db_insert_currency(reformatted)
        print(results[0])
    except Exception as e:
        print(f"Error in main: {e}")
    
get_data()