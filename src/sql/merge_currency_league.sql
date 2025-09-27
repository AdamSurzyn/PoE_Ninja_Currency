MERGE `${PROJECT}.${DATASET}.currency_leagues` AS T USING (
    SELECT DISTINCT league
    FROM `${PROJECT}.${DATASET}.currency_rates_stg`
) AS S ON T.league = S.league
WHEN MATCHED THEN
UPDATE
SET last_seen = TIMESTAMP_TRUNC(CURRENT_TIMESTAMP(), HOUR)
    WHEN NOT MATCHED THEN
INSERT (
        league,
        last_seen,
        first_seen
    )
VALUES(
        league,
        TIMESTAMP_TRUNC(CURRENT_TIMESTAMP(), HOUR),
        TIMESTAMP_TRUNC(CURRENT_TIMESTAMP(), HOUR)
    );