import psycopg2
import logging
def db_insert_currency_data():
    try:
        connection = psycopg2.connect(
            dbname="poe_currency",
            user="adam",
            host="localhost",
            port="5432"
            )
        cursor = connection.cursor()
        logging.info("Start currency insert.")
        insert_query = """
        INSERT INTO currency_rates (
            currency_type_name, 
            sample_time_utc,
            count,
            value_chaos
            )
        SELECT currency_type_name, sample_time_utc, count, value_chaos
        FROM currency_rates_stg_raw
                ON CONFLICT (currency_type_name, sample_time_utc)
        DO UPDATE SET
            count = EXCLUDED.count,
            value_chaos = EXCLUDED.value_chaos;
        """

        cursor.execute(insert_query)
        connection.commit()
    except Exception as e:
        logging.error(f"Error during currency insert: {e}")
        raise
    finally:
        cursor.close()
        connection.close()