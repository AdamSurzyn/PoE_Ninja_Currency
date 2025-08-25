from datetime import datetime
import re
import pandas as pd
import os
from sqlalchemy import create_engine
from google.cloud import bigquery

def format_sample_time(time_str):
    time_str = re.sub(r"Z$", "", time_str)
    time_str = re.sub(r"\.\d+", "", time_str)
    sample_time_utc = datetime.fromisoformat(time_str)
    return sample_time_utc.replace(minute=0, second=0, microsecond=0)

def reformat_dic(currency_dic, source, league):
    return {
        "currency_type_name": currency_dic["currencyTypeName"],
        "sample_time_utc": format_sample_time(currency_dic["receive"]["sample_time_utc"]),
        "count": currency_dic["receive"]["count"],
        "value_chaos": currency_dic["receive"]["value"],
        "detailsid": currency_dic["detailsId"],
        "source": source,
        "league": league
    }

def reformat_all_data(currency_items, source, league): 
    return [reformat_dic(item, source, league) for item in currency_items]


def save_csv_results(data):
    data_df = pd.DataFrame(data)
    data_df.to_csv("data_temp/settlers_currency_data.csv", index=False, mode='w')

def get_sqlalchemy_engine():
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT", 5432)
    db = os.getenv("DB_NAME")

    uri = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
    return create_engine(uri)

def _schema_to_bq(schema_tuples):
    return [bigquery.SchemaField(n, t, mode=m) for (n, t, m) in schema_tuples]