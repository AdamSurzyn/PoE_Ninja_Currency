import pandas as pd
from src.configs.schemas import BQ_TABLE_CONFIG
from dotenv import load_dotenv
from google.cloud import bigquery
from src.fetcher import get_poe_data
from src.utilities import format_sample_time, deduce_days, get_env_var, _render_sql_with_args, _schema_to_bq
from google.api_core.exceptions import NotFound

def getHistoricalData ():

    BASE_URL = 'https://poe.ninja/poe1/api/economy/stash/current/currency/overview?'
    source = "Historical"
    league = "Settlers"
    params = {
        "league": league,
        "type": "Currency"
    }
    HISTORICAL_BASE_URL = "https://poe.ninja/poe1/api/economy/stash/current/currency/history?"
    data_with_ids = get_poe_data(BASE_URL, params)["lines"]
    historical_items = []
    for item in data_with_ids:
        historical_params = {
            **params,
            "id": item["receive"]["get_currency_id"]
        }
        historical_items_data =get_poe_data(
            HISTORICAL_BASE_URL, 
            historical_params
        )
        
        sampleTime = format_sample_time(item["receive"]["sample_time_utc"])

        for historical_item in historical_items_data["receiveCurrencyGraphData"]:
            historical_item_daysAgo = historical_item["daysAgo"]
            historical_item_sample_time = deduce_days(sampleTime, historical_item_daysAgo) 
            historical_item_sample_time_midnight = historical_item_sample_time.replace(hour=0, minute=0, second=0, microsecond=0)

            historical_item_dic = {
            "currency_type_name": item["currencyTypeName"],
            "sample_time_utc": historical_item_sample_time_midnight,
            "count": historical_item["count"],
            "value_chaos": historical_item["value"],
            "detailsid": item["detailsId"],
            "source": source,
            "league": league
            }

            historical_items.append(historical_item_dic)
    return historical_items

def addHistoricalDataToStg(data, table_name):
    load_dotenv()
    project_id = get_env_var("GCP_PROJECT")
    dataset_id = get_env_var("BQ_DATASET")
    location = get_env_var("BQ_LOCATION")
    client = bigquery.Client(project=project_id, location=location)
    tableRef = bigquery.DatasetReference(project=project_id, dataset_id=dataset_id).table(table_name)
    bq_cfg_hist = BQ_TABLE_CONFIG[table_name]
    schema_hist = _schema_to_bq(bq_cfg_hist["schema"])
    try:
        client.get_table(tableRef)
    except NotFound:
        addHistoricalTable(client, dataset_id)
    
    poe_df = pd.DataFrame(data)
    poe_df["sample_time_utc"] = pd.to_datetime(poe_df["sample_time_utc"], utc=True)
    job_config = bigquery.LoadJobConfig(
        schema=schema_hist,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        ignore_unknown_values=True
    )
    job = client.load_table_from_dataframe(poe_df, tableRef, job_config=job_config)
    job.result()



def addHistoricalTable(client, dataset_id):
    path = "src/sql/addToTemp.sql"
    sql = _render_sql_with_args(path, client.project, dataset_id)
    job_config = bigquery.QueryJobConfig(
        use_legacy_sql=False,
    )
    job = client.query(sql, job_config=job_config)
    job.result()

def uploadHistoricalData():
    data = getHistoricalData()
    addHistoricalDataToStg(data, 'currency_rates_stg_historical')

if __name__ == "__main__":
    uploadHistoricalData()

