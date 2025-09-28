MERGE `${PROJECT}.${DATASET}.currency_sources` AS T USING (
    SELECT DISTINCT source
    FROM `${PROJECT}.${DATASET}.currency_rates_stg`
) AS S ON T.source = S.source
WHEN MATCHED THEN
UPDATE
SET last_seen = TIMESTAMP_TRUNC(CURRENT_TIMESTAMP(), HOUR)
    WHEN NOT MATCHED THEN
INSERT (
        source,
        last_seen,
        first_seen
    )
VALUES(
        source,
        TIMESTAMP_TRUNC(CURRENT_TIMESTAMP(), HOUR),
        TIMESTAMP_TRUNC(CURRENT_TIMESTAMP(), HOUR)
    );