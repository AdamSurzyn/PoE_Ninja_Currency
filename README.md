# PoE Ninja Currency Data Pipeline

A Python data pipeline for collecting and analyzing Path of Exile economy data using the poe.ninja API.

The project focuses on building a clean, reproducible workflow for ingesting external market data and preparing it for analytical use.

---

## Project Overview

Path of Exile has a player-driven economy without a single base currency. Item and currency values fluctuate over time depending on supply and demand.

This project fetches currency pricing data from the poe.ninja API, normalizes it, and prepares it for storage and analysis (e.g. in BigQuery or locally).

The goal is to model a real-world data ingestion pipeline rather than a game-specific tool.

---

## What This Project Does

- Fetches currency market data from the poe.ninja REST API  
- Normalizes and structures time-series data  
- Supports running as a standalone Python pipeline  
- Is container-ready via Docker  
- Is designed with analytics and further extensions in mind  

---

## Tech Stack

- Python  
- REST API integration  
- Docker  
- Environment-based configuration (`.env`)  
- Google Cloud Platform (BigQuery, Cloud Run Jobs)

---

## Running the Project Locally

```bash
git clone https://github.com/AdamSurzyn/PoE_Ninja_Currency.git
cd PoE_Ninja_Currency

python -m venv .venv
source .venv/bin/activate
pip install -r requirements/requirements.txt

python -m standalone.extract_run
```
---

## Project Structure

```text
├── src/                # Core pipeline logic
├── standalone/         # Standalone runner
├── tests/              # Tests (work in progress)
├── requirements/       # Python dependencies
├── Dockerfile
├── .env.example
└── README.md
```
---

## Tests

Basic test scaffolding is present, but the test suite is **not finished yet**.  
Improving test coverage is a planned next step.

---

## Next Steps / Planned Improvements

- Finish and expand automated tests  
- Add support for additional currency types  
- Extend the pipeline to fetch and process item data (not only currencies)  
- Improve schema validation and data quality checks  
- Add more example analytical queries  

---

## Why This Project

This project demonstrates practical data engineering skills:

- Working with external APIs  
- Designing a reusable data pipeline  
- Preparing data for analytical workloads  
- Structuring a project for future growth  

It is intentionally kept simple and focused on fundamentals rather than tooling overhead.
