import logging
from fetcher import get_poe_data
from db_insert import db_insert_currency
from utilities import reformat_all_data, save_csv_results

BASE_URL = 'https://poe.ninja/api/data/currencyoverview'
SETTLERS_PARAMS = {
    'league': 'Settlers',
    'type': 'Currency'  
}
def main():
    try:
        data = get_poe_data(BASE_URL, SETTLERS_PARAMS)
        if not data:
            logging.error("Data not received")
            return

        results = data["lines"]
        save_csv_results(results)

        reformatted = reformat_all_data(results)
        db_insert_currency(reformatted)
    except Exception as e:
        print(f"Error in main: {e}")