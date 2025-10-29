#Get item id's from ninja api
#Iterate through the id's
#It says how many days ago It needs to add date in this form 2025-10-12 17:00:00 UTC
#And get data before 15.07 to the beggining of the league.
#Run as normal insert with merges.
#Save as tool to get more leagues in dataset.
#Add items receive - get_id to the currencies dimensions table and staging.

import pandas as pa
from src.fetcher import get_poe_data
from src.utilities import format_sample_time

#receive
#get_currency_id

def getHistoricalData ():
    BASE_URL = 'https://poe.ninja/api/data/currencyoverview'
    source = "Historical"
    league = "Mercenaries"
    params = {
        "league": league,
        "type": "Currencies"
    }
    HISTORICAL_BASE_URL = "https://poe.ninja/api/data/currencyhistory"
    data_with_ids = get_poe_data(BASE_URL, params)["lines"]
    historical_items = []
    for item in data_with_ids:
        historical_params = {
            **params,
            "currencyId": item["receive"]["get_currency_id"]
        }
        historical_items_data =get_poe_data(
            HISTORICAL_BASE_URL, 
            historical_params
        )

        #Decide on the date from:to !!!

        for historical_item in historical_items_data["payCurrencyGraphData"]:
            historical_item_dic = {
            "currency_type_name": item["currencyTypeName"],
            "sample_time_utc": format_sample_time(item["receive"]["sample_time_utc"]),
            "count": historical_item["receive"]["count"],
            "value_chaos": historical_item["receive"]["value"],
            "detailsid": item["detailsId"],
            "source": source,
            "league": league
            }

        


