MERGE `${PROJECT}.${DATASET}.currency_rates_dim` as T USING (
    SELECT DISTINCT S.source,
        S.league,
        S.detailsid,
        S.currency_type_name
    FROM `${PROJECT}.${DATASET}.currency_rates_stg` S
    WHERE S.sample_time_utc >= @since
) as S ON T.source = S.source
AND T.league = S.league
AND T.currency_type_name = S.currency_type_name
WHEN MATCHED THEN
UPDATE
SET last_seen = CURRENT_TIMESTAMP()
    WHEN NOT MATCHED THEN
INSERT (
        detailsid,
        source,
        league,
        currency_type_name,
        first_seen,
        last_seen
    )
VALUES (
        S.detailsid,
        S.source,
        S.league,
        S.currency_type_name,
        CURRENT_TIMESTAMP(),
        CURRENT_TIMESTAMP()
    )