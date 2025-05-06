from fetcher import get_poe_data

BASE_URL = 'https://poe.ninja/api/data/currencyoverview'
SETTLERS_PARAMS = {
    'league': 'Settlers',
    'type': 'Currency'  
}

data = get_poe_data(BASE_URL, SETTLERS_PARAMS)

if data:
    print(data["lines"][0])