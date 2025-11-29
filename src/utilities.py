from datetime import datetime, timedelta
from google.cloud import bigquery
from pathlib import Path
from string import Template
import re
import os

def format_sample_time(time_str):
    time_str = re.sub(r"Z$", "", time_str)
    time_str = re.sub(r"\.\d+", "", time_str)
    sample_time_utc = datetime.fromisoformat(time_str)
    return sample_time_utc.replace(minute=0, second=0, microsecond=0)

def deduce_days(timeDateTime, days):
    return timeDateTime - timedelta(days=days)

def reformat_dic(currency_dic, source, league):
    return {
        "currency_type_name": currency_dic["currencyTypeName"],
        "sample_time_utc": format_sample_time(currency_dic["receive"]["sample_time_utc"]),
        "count": currency_dic["receive"]["count"],
        "value_chaos": currency_dic["receive"]["value"],
        "detailsid": currency_dic["detailsId"],
        "source": source,
        "league": league
    }

def reformat_all_data(currency_items, source, league): 
    return [reformat_dic(item, source, league) for item in currency_items]


def _schema_to_bq(schema_tuples):
    return [bigquery.SchemaField(n, t, mode=m) for (n, t, m) in schema_tuples]

def get_env_var(name):
    value = os.getenv(name)
    if not value:
        raise EnvironmentError(f"Missing required environment variable: {name}")
    return value

def _render_sql_with_args(path, project, dataset):
    sql_path = Path(path)
    if not sql_path.exists:
        raise FileNotFoundError(f"SQL file not found: {sql_path}")
    txt = sql_path.read_text(encoding="utf-8")
    return Template(txt).substitute(PROJECT=project, DATASET=dataset)