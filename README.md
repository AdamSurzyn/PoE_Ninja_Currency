PoE Ninja Currency Data Pipeline

A lightweight data pipeline for extracting Path of Exile currency data from the PoE Ninja API and loading it into BigQuery for analysis.

Overview

This project fetches currency exchange data every hour, stores it in a staging table, and merges it into fact and dimension tables using SQL MERGE statements.

The pipeline runs locally or on Google Cloud Run and is designed to be simple, modular, and cost-efficient.

Architecture
PoE Ninja API → Cloud Run (Python App) → BigQuery

Tables
Layer Table Description
Staging currency_rates_stg Raw hourly currency data
Dimension currency_rates_dim Currency metadata and tracking (first_seen, last_seen)
Fact currency_rates Hourly prices and counts per currency and league
Tech Stack

Python 3.11

BigQuery

Google Cloud Run

Docker

dotenv for environment configuration

Local Setup

1. Clone the repository
   git clone https://github.com/<your-username>/PoE_Ninja_Currency.git
   cd PoE_Ninja_Currency

2. Set environment variables

Create a .env file:

GCP_PROJECT=poeninjacurrencydata
BQ_DATASET=poe
BQ_LOCATION=europe-central2

3. Install dependencies
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements/requirements.txt

4. Run the pipeline locally
   python -m standalone.extract_run

You can also trigger your merge steps manually:

python -m src.db_inserts.run_dim_merge
python -m src.db_inserts.run_fact_merge

Deployment (Cloud Run)

Build and deploy your container:

gcloud builds submit --tag gcr.io/$GCP_PROJECT/poe-ninja-currency
gcloud run deploy poe-ninja \
  --image gcr.io/$GCP_PROJECT/poe-ninja-currency \
 --region europe-central2 \
 --set-env-vars GCP_PROJECT=$GCP_PROJECT,BQ_DATASET=$BQ_DATASET,BQ_LOCATION=$BQ_LOCATION \
 --no-allow-unauthenticated

Example Query
SELECT
currency_type_name,
AVG(value_chaos) AS avg_price,
league
FROM `poe.currency_rates`
WHERE sample_time_utc > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
GROUP BY currency_type_name, league
ORDER BY avg_price DESC;

Project Structure
.
├── src/
│ ├── configs/
│ ├── db_inserts/
│ ├── fetcher.py
│ ├── utilities.py
│ └── ...
├── standalone/
│ └── extract_run.py
├── requirements/
│ └── requirements.txt
├── Dockerfile
└── README.md

Notes

BigQuery tables are partitioned and clustered for cost efficiency.

The merge process is idempotent: it updates existing rows and inserts new ones.

Designed for minimal operational overhead (< $1/month to run).
