MERGE `${PROJECT}.${DATASET}.currency_rates` as T USING (
    SELECT S.league,
        S.sample_time_utc,
        MAX(S.count) as count,
        AVG(S.value_chaos) as value_chaos,
        S.currency_type_name
    FROM `${PROJECT}.${DATASET}.currency_rates_stg` S
    WHERE S.sample_time_utc >= @since
    GROUP BY league,
        sample_time_utc,
        currency_type_name
) as S ON T.currency_type_name = S.currency_type_name
AND T.sample_time_utc = S.sample_time_utc
AND T.league = S.league
WHEN MATCHED THEN
UPDATE
SET count = S.count,
    value_chaos = S.value_chaos,
    inserted_at = TIMESTAMP_TRUNC(CURRENT_TIMESTAMP(), HOUR)
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
        TIMESTAMP_TRUNC(CURRENT_TIMESTAMP(), HOUR)
    )