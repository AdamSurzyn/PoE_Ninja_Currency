from fetcher import get_poe_data
from db_insert import db_insert_currency
from utilities import reformat_all_data
import pandas as pd

BASE_URL = 'https://poe.ninja/api/data/currencyoverview'
SETTLERS_PARAMS = {
    'league': 'Settlers',
    'type': 'Currency'  
}

data = get_poe_data(BASE_URL, SETTLERS_PARAMS)
if data:
    results = data["lines"]
    poe_df = pd.DataFrame(results)
    poe_df.to_csv("data_temp/settlers_currency_data.csv", index=False)
    results_reform = reformat_all_data(results)
    print(type(results_reform))
    print(results_reform[0])
    db_insert_currency(results_reform)