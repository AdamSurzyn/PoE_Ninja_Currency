from fetcher import get_poe_data
from db_insert import db_insert_currency
from utilities import reformat_all_data
import pandas as pd

BASE_URL = 'https://poe.ninja/api/data/currencyoverview'
SETTLERS_PARAMS = {
    'league': 'Settlers',
    'type': 'Currency'  
}
def main():
    try:
        data = get_poe_data(BASE_URL, SETTLERS_PARAMS)
        if not data:
            print("No data received.")
            return

        results = data["lines"]
        poe_df = pd.DataFrame(results)
        poe_df.to_csv("data_temp/settlers_currency_data.csv", index=False)

        reformatted = reformat_all_data(results)
        db_insert_currency(reformatted)
    except Exception as e:
        print(f"Error in main: {e}")