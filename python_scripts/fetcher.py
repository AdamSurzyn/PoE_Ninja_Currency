import requests

url_cur = 'https://poe.ninja/api/data/currencyoverview'
params_set = {
    'league': 'Kettlers',
    'type': 'Currency'
}
def get_poe_request(url, params):
    if url is not None and params is not None:

        try:
            currency_res = requests.get(url, params)
            currency_res.raise_for_status()
            return currency_res.json()
        except requests.exceptions.RequestException as er:
            print(f"Error fetching data: {er}")
            return None
        except ValueError as er: 
            print(f"Error parsing JSON: {er}")
    else: 
        raise Exception("One of the parameters is empty in requesting function.")
    
result = get_poe_request(url_cur, params_set)
print(result)