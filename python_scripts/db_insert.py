import psycopg2
from collections import namedtuple
from datetime import date, datetime
from utilities import format_sample_time

json_data = {
  "currencyTypeName": "Mirror of Kalandra",
  "receive": {
    "sample_time_utc": "2025-05-08T10:34:41.9799164Z",
    "count": 28,
    "value": 153054.66564
  },
  "detailsId": "mirror-of-kalandra"
}

def db_insert_currency(currency_data):
    sample_time_utc = format_sample_time(currency_data["receive"]["sample_time_utc"])

    connection = psycopg2.connect(
        dbname="poe_currency",
        user="adam",
        host="localhost",
        port="5432"
        )
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO currency_rates (
        currency_type_name, 
        sample_time_utc, 
        count, 
        value_chaos, 
        detailsId
        )
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (currency_type_name, sample_time_utc)
    DO UPDATE SET
        count = EXCLUDED.count,
        value_chaos = EXCLUDED.value_chaos,
        detailsId = EXCLUDED.detailsId;
    """, (
    currency_data['currencyTypeName'],
    sample_time_utc,
    currency_data['receive']['count'],
    currency_data['receive']['value'],
    currency_data['detailsId']
    ))
    connection.commit()

db_insert_currency(json_data)