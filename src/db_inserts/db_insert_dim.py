from sqlalchemy import Table, MetaData, select, distinct
from sqlalchemy.dialects.postgresql import insert
from src.utilities import get_sqlalchemy_engine
import logging

def db_insert_currency_dim():
  try:
    engine = get_sqlalchemy_engine()
    metaData = MetaData()
    currencyDimTable = Table("currency_rates_dim", metaData, autoload_with=engine)
    stagingTable = Table("currency_rates_stg_raw", metaData, autoload_with=engine)

    stg_select = select(stagingTable.c.currency_type_name, stagingTable.c.source, stagingTable.c.league).distinct()

    stmt = insert(currencyDimTable).from_select([currencyDimTable.c.currency_type_name, currencyDimTable.c.source, currencyDimTable.c.league], stg_select)

    stmt = stmt.on_conflict_do_nothing()

    with engine.begin() as conn: conn.execute(stmt)
  except Exception as e:
    logging.error(f"Error during dim insert: {e}")
    raise