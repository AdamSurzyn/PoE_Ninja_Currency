MERGE `${PROJECT}.${DATASET}.currency_rates` AS T USING (
    SELECT S.league,
        S.sample_time_utc,
        MAX(S.count) AS count,
        AVG(S.value_chaos) AS value_chaos,
        S.currency_type_name,
        DATE_DIFF(
            DATE(S.sample_time_utc),
            DATE(L.league_start_timestamp),
            DAY
        ) AS days_since_league_start
    FROM `${PROJECT}.${DATASET}.currency_rates_stg` S
        JOIN `${PROJECT}.${DATASET}.currency_leagues_dim` L ON S.league = L.league
    WHERE S.sample_time_utc >= @since
        AND L.league_start_timestamp IS NOT NULL
        AND DATE(S.sample_time_utc) >= DATE(L.league_start_timestamp)
    GROUP BY S.league,
        S.sample_time_utc,
        S.currency_type_name,
        L.league_start_timestamp
) AS S ON T.currency_type_name = S.currency_type_name
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
        inserted_at,
        days_since_league_start
    )
VALUES (
        S.league,
        S.sample_time_utc,
        S.count,
        S.value_chaos,
        S.currency_type_name,
        TIMESTAMP_TRUNC(CURRENT_TIMESTAMP(), HOUR),
        S.days_since_league_start
    );