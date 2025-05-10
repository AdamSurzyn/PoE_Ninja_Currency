from datetime import datetime
import re
import json

def format_sample_time(time_str):
    sample_time_iso = re.sub(r"\.\d+Z", "", time_str)
    sample_time_utc = datetime.fromisoformat(sample_time_iso)
    sample_time_hour = sample_time_utc.replace(minute=0, second=0, microsecond=0)
    return sample_time_hour

def reformat_dic(currency_dic):
    return (
        currency_dic['currencyTypeName'],
        format_sample_time(currency_dic["receive"]["sample_time_utc"]),
        currency_dic["receive"]["count"],
        currency_dic["receive"]["value"],
        currency_dic["detailsId"]
    )

def reformat_all_data(currency_items): 
    formatted_items = []
    for currency_item in currency_items:
        formatted_item = reformat_dic(currency_item)
        formatted_items.append(formatted_item)
    return formatted_items