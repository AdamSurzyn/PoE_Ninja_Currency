MERGE `${PROJECT}.${DATASET}.currency_rates` as T USING (
    SELECT DISTINCT S.league,
        S.sample_time_utc,
        S.count,
        S.value_chaos,
        S.currency_type_name
    FROM `${PROJECT}.${DATASET}.currency_rates_stg` S
    WHERE S.sample_time_utc >= @since
) as S ON T.currency_type_name = S.currency_type_name
AND T.sample_time_utc = S.sample_time_utc
AND T.league = S.league
WHEN MATCHED THEN
UPDATE
SET count = S.count,
    value_chaos = S.value_chaos
    WHEN NOT MATCHED THEN
INSERT (
        league,
        sample_time_utc,
        count,
        value_chaos,
        currency_type_name,
        inserted_at
    )
VALUES (
        S.league,
        S.sample_time_utc,
        S.count,
        S.value_chaos,
        S.currency_type_name,
        CURRENT_TIMESTAMP()
    )