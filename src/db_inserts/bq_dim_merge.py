import logging
from google.cloud import bigquery
from google.cloud.bigquery import QueryJobConfig, ScalarQueryParameter
from src.utilities import get_env_var, _render_sql_with_args
from datetime import datetime, timezone, timedelta

def run_poe_merge(path, since_ts=None):

    project_id = get_env_var("GCP_PROJECT")
    dataset_id = get_env_var("BQ_DATASET")
    location = get_env_var("BQ_LOCATION")
    try:
        sql = _render_sql_with_args(path, project_id, dataset_id)
        if since_ts is None:
            since_ts = datetime.now(timezone.utc) - timedelta(hours=2)

        job_config = QueryJobConfig(
            use_legacy_sql=False,
            query_parameters=[
                ScalarQueryParameter("since", "TIMESTAMP", since_ts) #Scalar - so we just pass one value, very smart naming.
            ],
        )

        client = bigquery.Client(project=project_id)
        logging.info(f"Running MERGE from {path} in project={client.project}, dataset={dataset_id}, location={location}, since={since_ts.isoformat()}")
        job = client.query(sql, job_config=job_config)
        job.result()
        logging.info("facts MERGE completed.")
    except Exception as e:
        logging.error(f"Error during raw data insert: {e}")
        raise

    