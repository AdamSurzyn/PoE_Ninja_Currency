import requests
def get_poe_data(url, params):
    if not url or not params:
        raise ValueError("URL or parameters are missing")
    try:
        currency_res = requests.get(url, params, timeout= 60000)
        currency_res.raise_for_status()
        return currency_res.json()
    except requests.exceptions.RequestException as er:
        print(f"Error fetching data: {er}")
        return None
    except ValueError as er: 
        print(f"Error parsing JSON: {er}")

