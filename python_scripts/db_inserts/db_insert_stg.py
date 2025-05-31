import logging
import psycopg2
import psycopg2.extras

def db_insert_currency(currency_data):

    connection = psycopg2.connect(
        dbname="poe_currency",
        user="adam",
        host="localhost",
        port="5432"
        )
    cursor = connection.cursor()
    logging.INFO("Start dim insert.")
    insert_query = """
    INSERT INTO currency_rates_stg_raw (
        currency_type_name, 
        sample_time_utc, 
        count, 
        value_chaos, 
        detailsId,
        source,
        league
        )
      VALUES %s
      ON CONFLICT (currency_type_name, sample_time_utc)
      DO UPDATE SET
        count = EXCLUDED.count,
        value_chaos = EXCLUDED.value_chaos,
        detailsId = EXCLUDED.detailsId;
    """
    psycopg2.extras.execute_values (
        cursor, insert_query, currency_data
    )
    connection.commit()
    cursor.close()
    connection.close()