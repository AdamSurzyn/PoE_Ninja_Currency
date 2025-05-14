from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from python_scripts.main import main
import sys
print("PYTHONPATH:", sys.path)
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
    task_id="get_settlers_currency_data",
    python_callable=main,
    dag=dag
)