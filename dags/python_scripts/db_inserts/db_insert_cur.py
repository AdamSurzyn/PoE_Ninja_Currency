from sqlalchemy import create_engine, Table, MetaData, select
from sqlalchemy.dialects.postgresql import insert
from airflow.hooks.base import BaseHook
import logging




def db_insert_currency_data():
    try:
        airConn = BaseHook.get_connection("poe_postgres_conn")
        airUri = airConn.get_uri()
        airUri = airUri.replace("postgres://", "postgresql+psycopg2://", 1) #JEEEEEEEEEEESUS, THATS INSANE
        engine = create_engine(airUri)
        metaData = MetaData()
        currencyTable = Table("currency_rates", metaData, autoload_with=engine)
        stagingTable = Table("currency_rates_stg_raw", metaData, autoload_with=engine)

        stg_select = select(stagingTable.c.currency_type_name, stagingTable.c.sample_time_utc, stagingTable.c.count, stagingTable.c.value_chaos)

        stmt = insert(currencyTable).from_select([currencyTable.c.currency_type_name, currencyTable.c.sample_time_utc, currencyTable.c.count, currencyTable.c.value_chaos], stg_select)

        stmt = stmt.on_conflict_do_update(index_elements=[currencyTable.c.currency_type_name, currencyTable.c.sample_time_utc], set_={"count": stmt.excluded.count, "value_chaos": stmt.excluded.value_chaos})

        with engine.begin() as conn: conn.execute(stmt)

    except Exception as e:
        logging.error(f"Error during currency insert: {e}")
        raise