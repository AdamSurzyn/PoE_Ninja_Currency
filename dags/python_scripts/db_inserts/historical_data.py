import requests


def get_ids_dic():
    url = "https://poe.ninja/api/data/currencyoverview?league=Settlers&type=Currency"
    currency_res = requests.get(url, timeout= 60000)
    currency_res.raise_for_status()
    currency_json = currency_res.json()["lines"]
    ids_name_dic = {}

    for line in currency_json:
        ids_name_dic[line["currencyTypeName"]] = line["receive"]["get_currency_id"]
    print(ids_name_dic)
    return ids_name_dic

get_ids_dic()
