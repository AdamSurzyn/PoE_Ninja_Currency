from sqlalchemy import text
from python_scripts.utilities import get_sqlalchemy_engine

LOCK_ID = 36549087

def acquire_job_lock(engine):

    engine = engine or get_sqlalchemy_engine()
    conn = engine.connect()
    got = conn.execute(
        text("SELECT pg_try_advisory_lock(:id)"),
        {"id": LOCK_ID},
    ).scalar() # scalar essentialy picks first row first column value (true or false)
    if not got:
        conn.close()
        return None
    return conn

def release_job_lock(lock_conn):

    if lock_conn is None:
        return
    try:
        lock_conn.execute(text("SELECT pg_advisory_unlock(:id)"), {"id": LOCK_ID})
    finally:
        lock_conn.close()