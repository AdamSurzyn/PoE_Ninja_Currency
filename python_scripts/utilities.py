from datetime import datetime
import re
import json

def format_sample_time(time_str):
    sample_time_iso = re.sub(r"\.\d+Z", "", time_str)
    sample_time_utc = datetime.fromisoformat(sample_time_iso)
    sample_time_hour = sample_time_utc.replace(minute=0, second=0, microsecond=0)
    return sample_time_hour

def reformat_dic(currency_response):
    currency_dic = decode_json(currency_response)
    return {
        "currency_type_name": currency_dic['currencyTypeName'],
        "sample_time_utc": currency_dic["receive"]["sample_time_utc"],
        "count": currency_dic["receive"]["count"],
        "value": currency_dic["receive"]["value"],
        "details_id": currency_dic["detailsId"]
    }

def decode_json(sample):

    try:
        dic_sample = json.loads(sample)
    except:
        return dic_sample

    return sample

def reformat_all_data(currency_items): 
    formatted_items = []
    for currency_item in currency_items:
        formatted_item = reformat_dic(currency_item)
        formatted_items.append(formatted_item)
    return formatted_items