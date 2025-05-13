from airflow import DAG
from airflow.operators.empty import EmptyOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 5, 13),
    'retries': 1
}

dag = DAG(
    dag_id='poe_settlers_dag',
    default_args=default_args,
    description='dag that will download and save data regarding phrecia currencies',
    schedule_interval=None
)

start_task = EmptyOperator(
    task_id='start_task',
    dag=dag,
)

end_task = EmptyOperator(
    task_id='end_task',
    dag=dag,
)

start_task >> end_task