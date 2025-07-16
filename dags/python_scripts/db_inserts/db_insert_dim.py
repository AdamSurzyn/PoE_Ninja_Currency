import psycopg2
import logging
def db_insert_currency_dim():
  try:
    connection = psycopg2.connect(
        dbname="poe_currency",
        user="adam",
        host="localhost",
        port="5432"
        )
    cursor = connection.cursor()
    logging.info("Start raw data insert.")
    insert_query = """
    INSERT INTO currency_rates_dim (
        currency_type_name, 
        source,
        league 
        )
      SELECT DISTINCT currency_type_name, source, league
      FROM currency_rates_stg_raw
      ON CONFLICT (currency_type_name, source, league) DO NOTHING;
    """

    cursor.execute(insert_query)
    connection.commit()
  except Exception as e:
    logging.error(f"Error during dim insert: {e}")
    raise
  finally:
    cursor.close()
    connection.close()