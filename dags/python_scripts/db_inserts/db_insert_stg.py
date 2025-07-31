from sqlalchemy import Table, MetaData, select
from sqlalchemy.dialects.postgresql import insert
from python_scripts.utilities import get_sqlalchemy_engine
import logging

def db_insert_currency(currency_data):
    try:
        engine = get_sqlalchemy_engine()
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