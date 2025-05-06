from fetcher import get_poe_data
import pandas as pd
BASE_URL = 'https://poe.ninja/api/data/currencyoverview'
SETTLERS_PARAMS = {
    'league': 'Settlers',
    'type': 'Currency'  
}

data = get_poe_data(BASE_URL, SETTLERS_PARAMS)
if data:
    results = data["lines"]
    print(data["lines"][0])
    poe_df = pd.DataFrame(results)
    poe_df.to_csv("data_temp/settlers_currency_data.csv", index=False)