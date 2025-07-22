FROM apache/airflow:2.9.1-python3.10-slim

COPY requirements.txt .

USER root
RUN pip install --no-cache-dir -r requirements.txt
USER airflow