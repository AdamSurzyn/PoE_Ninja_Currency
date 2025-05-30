from datetime import datetime
import re
import pandas as pd

def format_sample_time(time_str):
    sample_time_iso = re.sub(r"\.\d+Z", "", time_str)
    sample_time_utc = datetime.fromisoformat(sample_time_iso)
    return sample_time_utc.replace(minute=0, second=0, microsecond=0)

def reformat_dic(currency_dic, source):
    return (
        currency_dic['currencyTypeName'],
        format_sample_time(currency_dic["receive"]["sample_time_utc"]),
        currency_dic["receive"]["count"],
        currency_dic["receive"]["value"],
        currency_dic["detailsId"],
        source
    )

def reformat_all_data(currency_items, source): 
    formatted_items = []
    for currency_item in currency_items:
        formatted_item = reformat_dic(currency_item, source)
        formatted_items.append(formatted_item)
    return formatted_items

def save_csv_results(data):
    data_df = pd.DataFrame(data)
    data_df.to_csv("data_temp/settlers_currency_data.csv", index=False, mode='w')