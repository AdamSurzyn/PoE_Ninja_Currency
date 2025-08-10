from datetime import datetime
import logging
import os
import psycopg2
import psycopg2.extras
import requests
import pandas as pd
import time

def fetch_currency_history_pd(data_dic, output_path="currency_history.csv", days_limit=60, delay=1.0):
    base_url = "https://poe.ninja/api/data/currencyhistory"
    league = "Settlers"
    type_ = "Currency"
    today = pd.to_datetime(datetime.utcnow().date()) 
    all_data = []

    for currency_name, currency_id in data_dic.items():
        url = f"{base_url}?league={league}&type={type_}&currencyId={currency_id}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            entries = data["receiveCurrencyGraphData"]

            df = (
                pd.DataFrame(entries)
                .loc[lambda d: d["daysAgo"] <= days_limit] #Filters out rows before days limit - probably should've done it in sql.
                .rename(columns={"value": "value_chaos"})
            )

            df = df.assign(
                currency_type_name=currency_name,
                source="Historical",
                league=league,
                detailsid=None,
                sample_time_utc=(today - pd.to_timedelta(df["daysAgo"], unit="D")).dt.date
            ).drop(columns=["daysAgo"])

            df = df[[
                "currency_type_name",
                "sample_time_utc",
                "count",
                "value_chaos",
                "detailsid",
                "source",
                "league"
            ]]

            all_data.append(df)

        except Exception as e:
            print(f"Error processing '{currency_name}' (ID: {currency_id}): {e}")
        time.sleep(delay)

        if all_data:
            final_df = pd.concat(all_data, ignore_index=True)
            final_df = final_df[["currency_type_name", "sample_time_utc", "count", "value_chaos", "detailsid", "source", "league"]]
            final_df.to_csv(output_path, index=False, mode="w", na_rep="NULL")
            print(f"Data saved to file: {output_path}")
        else:
            print("No data to save.")

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

def find_data_temp(start_path=None):
    current = start_path or os.path.abspath(os.path.dirname(__file__))
    while True:
        candidate = os.path.join(current, "data_temp")
        if os.path.isdir(candidate):
            return os.path.abspath(candidate)
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent
    return None

def db_insert_currency_historical():
    df = pd.read_csv("data_temp/historical_settlers_currency_data.csv")
    df = df.where(pd.notnull(df), None)
    values = df.values.tolist()
    try:
        connection = psycopg2.connect(
            dbname="poe_currency",
            user="adam",
            host="localhost",
            port="5432"
            )
        cursor = connection.cursor()
        logging.info("Start dim insert.")
        insert_query = """
        INSERT INTO currency_rates_stg_raw (
            currency_type_name, 
            sample_time_utc, 
            count, 
            value_chaos, 
            detailsid,
            source,
            league
            )
        VALUES %s
        ON CONFLICT (currency_type_name, sample_time_utc)
        DO UPDATE SET
            count = EXCLUDED.count,
            value_chaos = EXCLUDED.value_chaos,
            detailsId = EXCLUDED.detailsid;
        """
        psycopg2.extras.execute_values (
            cursor, insert_query, values
        )
        connection.commit()
    except Exception as e:
        logging.error(f"Error during raw data insert: {e}")
        raise
    finally:
        cursor.close()
        connection.close()

HISTORICAL_DATA = get_ids_dic()
fetch_currency_history_pd(HISTORICAL_DATA, "data_temp/historical_settlers_currency_data.csv")
db_insert_currency_historical()

#TODO: ADD CONCURRENT REQUESTS
#TODO: SIMPLIFY