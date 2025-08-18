from sqlalchemy import Table, MetaData, select
from sqlalchemy.dialects.postgresql import insert
from src.utilities import get_sqlalchemy_engine
import logging

REQUIRED_STG = {
    "currency_type_name", "detailsid", "sample_time_utc",
    "count", "value_chaos", "source", "league"
}

def db_insert_currency(currency_data):
    try:
        if not currency_data:
            logging.info("staging: nothing to insert"); 
            return  
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