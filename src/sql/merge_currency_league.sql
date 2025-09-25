MERGE "${PROJECT}.${DATASET}.leagues" AS T USING (
    SELECT DISTINCT S.league
    FROM "${PROJECT}.${DATASET}.currency_rates_stg"
) AS S ON T.league = S.league
WHEN MATCHED THEN
UPDATE
SET last_seen = CURRENT_TIMESTAMP()
    WHEN NOT MATCHED THEN
INSERT (
        league,
        last_seen = CURRENT_TIMESTAMP(),
        first_seen = CURRENT_TIMESTAMP()
    )
VALUES(
        S.league,
        CURRENT_TIMESTAMP(),
        CURRENT_TIMESTAMP()
    );