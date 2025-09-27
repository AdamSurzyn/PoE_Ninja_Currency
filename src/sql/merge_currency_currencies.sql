MERGE `${PROJECT}.${DATASET}.currency_currencies` AS T USING (
    SELECT DISTINCT currency_type_name
    FROM `${PROJECT}.${DATASET}.currency_rates_stg`
) AS S ON T.currency_type_name = S.currency_type_name
WHEN MATCHED THEN
UPDATE
SET last_seen = TIMESTAMP_TRUNC(CURRENT_TIMESTAMP(), HOUR)
    WHEN NOT MATCHED THEN
INSERT (
        currency_type_name,
        last_seen,
        first_seen
    )
VALUES(
        currency_type_name,
        TIMESTAMP_TRUNC(CURRENT_TIMESTAMP(), HOUR),
        TIMESTAMP_TRUNC(CURRENT_TIMESTAMP(), HOUR)
    );