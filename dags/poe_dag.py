import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
    
from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from python_scripts.extract_load import get_data
from python_scripts.db_inserts.db_insert_dim import db_insert_currency_dim

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 5, 13),
    'retries': 1
}

dag = DAG(
    dag_id='poe_dag',
    default_args=default_args,
    description='dag that will download and save data regarding phrecia currencies',
    schedule_interval='@daily',
    catchup=False
)
# For now it's all in one step because there is not much data.
# Later when I will learn how I will divide  it into steps.
update_data = PythonOperator(
    task_id="get_currency_data",
    python_callable=get_data,
    dag=dag
)

update_dim = PythonOperator(
    task_id="update_currency_data",
    python_callable=db_insert_currency_dim,
    dag=dag
)

update_data >> update_dim