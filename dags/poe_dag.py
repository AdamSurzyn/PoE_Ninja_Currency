from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from python_scripts.extract_load import get_data
from python_scripts.db_inserts.db_insert_dim import db_insert_currency_dim
from python_scripts.db_inserts.db_insert_cur import db_insert_currency_data

print(f"db_insert_currency_data type: {type(db_insert_currency_data)}")
print(f"db_insert_currency_dim type: {type(db_insert_currency_dim)}")
print(f"get_data type: {type(get_data)}")

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
    task_id="get_raw_data",
    python_callable=get_data,
    dag=dag
)

update_dim = PythonOperator(
    task_id="update_dim",
    python_callable=db_insert_currency_dim,
    dag=dag
)

update_currency = PythonOperator(
    task_id="update_currency_data",
    python_callable=db_insert_currency_data,
    dag=dag
)
update_data >> update_dim >> update_currency