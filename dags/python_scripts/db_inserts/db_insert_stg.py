from sqlalchemy import create_engine, Table, MetaData, select
from sqlalchemy.dialects.postgresql import insert
from airflow.hooks.base import BaseHook
import logging

def db_insert_currency(currency_data):
    try:
        airConn = BaseHook.get_connection("poe_postgres_conn")
        airUri = airConn.get_uri()
        airUri = airUri.replace("postgres://", "postgresql+psycopg2://", 1) 
        engine = create_engine(airUri)
        metaData = MetaData()
        stagingTable = Table("currency_rates_stg_raw", metaData, autoload_with=engine)
        logging.info("Start dim insert.")

        stmt = insert(stagingTable).values(currency_data)
        stmt = stmt.on_conflict_do_nothing()

        with engine.begin() as conn:
            conn.execute(stmt)

    except Exception as e:
        logging.error(f"Error during raw data insert: {e}")
        raise