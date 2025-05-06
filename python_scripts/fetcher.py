import requests
from logger import setup_logger

def get_poe_data(url, params):
    if not url or not params:
        raise ValueError("URL or parameters are missing")
    try:
        currency_res = requests.get(url, params)
        currency_res.raise_for_status()
        setup_logger('poe_get.log')
        return currency_res.json()
    except requests.exceptions.RequestException as er:
        print(f"Error fetching data: {er}")
        return None
    except ValueError as er: 
        print(f"Error parsing JSON: {er}")

