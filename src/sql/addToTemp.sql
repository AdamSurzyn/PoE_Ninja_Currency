CREATE TABLE `${PROJECT}.${DATASET}.currency_rates_stg_historical` (
    currency_type_name STRING NOT NULL,
    source STRING NOT NULL,
    detailsid STRING,
    league STRING NOT NULL,
    sample_time_utc TIMESTAMP NOT NULL,
    count INT64 NOT NULL,
    value_chaos FLOAT64
);