BQ_TABLE_CONFIG = {
    "currency_rates_stg": {
        "schema": [
            ("currency_type_name", "STRING",    "REQUIRED"),
            ("source",             "STRING",    "REQUIRED"),
            ("detailsid",          "STRING",    "NULLABLE"),
            ("league",             "STRING",    "REQUIRED"),
            ("sample_time_utc",    "TIMESTAMP", "REQUIRED"),
            ("count",              "INT64",     "REQUIRED"),
            ("value_chaos",        "FLOAT64",   "NULLABLE"),
        ],

        "conflict_key": (
            "currency_type_name",
            "detailsid",
            "sample_time_utc",
            "source",
            "league"
        ),
    },
}