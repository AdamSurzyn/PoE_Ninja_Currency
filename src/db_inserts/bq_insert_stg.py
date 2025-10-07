from src.configs.schemas import BQ_TABLE_CONFIG
from src.utilities import _schema_to_bq, get_env_var
from google.cloud import bigquery
from google.api_core.exceptions import NotFound
import pandas as pd
import logging

def db_insert_currency(currency_data,
                       table_name):
    try:
        if not currency_data:
            logging.info("staging: nothing to insert"); 
            return  
        if table_name not in BQ_TABLE_CONFIG:
            raise KeyError(f"Unknown table in BQ_TABLE_CONFIG: {table_name}")
        
        bq_cfg_stg = BQ_TABLE_CONFIG[table_name]
        project_id = get_env_var("GCP_PROJECT")
        dataset_id = get_env_var("BQ_DATASET")
        schema_stg = _schema_to_bq(bq_cfg_stg["schema"])
    
        client = bigquery.Client(project=project_id)
        table_ref = bigquery.DatasetReference(project_id, dataset_id).table(table_name)

        logging.info(f"BQ target: project={client.project} dataset={dataset_id} table={table_name} loc={client.location}")

        try:
            client.get_table(table_ref)
        except NotFound:
            raise RuntimeError(f"Table {table_ref.path} does not exist. (We don't create tables here.)")

        poe_df = pd.DataFrame(currency_data)
        poe_df["sample_time_utc"] = pd.to_datetime(poe_df["sample_time_utc"], utc=True)

        job_config = bigquery.LoadJobConfig(
            schema=schema_stg,
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
            ignore_unknown_values=True
        )
        load_job = client.load_table_from_dataframe(poe_df, table_ref, job_config=job_config)
        load_job.result()
        logging.info(f"Loaded {load_job.output_rows} rows into {table_ref.path}")

    except Exception as e:
        logging.error(f"Error during raw data insert: {e}")
        raise