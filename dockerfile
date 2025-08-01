FROM apache/airflow:2.9.1-python3.10-slim

COPY requirements/requirements.txt .
COPY requirements/requirements-airflow.txt .
USER root
RUN pip install --no-cache-dir \
    -r requirements/requirements.txt \
    -r requirements/requirements-airflow.txt
USER airflow