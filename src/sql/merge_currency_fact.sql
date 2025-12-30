MERGE `${PROJECT}.${DATASET}.currency_rates` AS T USING (
    WITH aggregated AS (
        SELECT S.league,
            S.sample_time_utc,
            MAX(S.count) AS count,
            AVG(S.value_chaos) AS value_chaos,
            S.currency_type_name,
            DATE_DIFF(
                DATE(S.sample_time_utc),
                DATE(L.league_start),
                DAY
            ) AS days_since_league_start
        FROM `${PROJECT}.${DATASET}.currency_rates_stg` S
            JOIN `${PROJECT}.${DATASET}.currency_leagues_dim` L ON S.league = L.league
        WHERE S.sample_time_utc >= @since
            AND L.league_start IS NOT NULL
            AND DATE(S.sample_time_utc) >= DATE(L.league_start)
        GROUP BY S.league,
            S.sample_time_utc,
            S.currency_type_name,
            L.league_start
    )
    SELECT S.league,
        S.sample_time_utc,
        S.count,
        S.value_chaos,
        S.currency_type_name,
        S.days_since_league_start,
        ROUND(
            STDDEV(S.value_chaos) OVER (
                PARTITION BY S.league,
                S.currency_type_name
                ORDER BY UNIX_SECONDS(S.sample_time_utc) RANGE BETWEEN 604800 PRECEDING AND CURRENT ROW
            ),
            2
        ) AS chaos_price_std_7d
    FROM aggregated AS S
) AS S ON T.currency_type_name = S.currency_type_name
AND T.sample_time_utc = S.sample_time_utc
AND T.league = S.league
WHEN MATCHED THEN
UPDATE
SET count = S.count,
    value_chaos = S.value_chaos,
    chaos_price_std_7d = S.chaos_price_std_7d,
    inserted_at = TIMESTAMP_TRUNC(CURRENT_TIMESTAMP(), HOUR)
    WHEN NOT MATCHED THEN
INSERT (
        league,
        sample_time_utc,
        count,
        value_chaos,
        currency_type_name,
        inserted_at,
        days_since_league_start,
        chaos_price_std_7d
    )
VALUES (
        S.league,
        S.sample_time_utc,
        S.count,
        S.value_chaos,
        S.currency_type_name,
        TIMESTAMP_TRUNC(CURRENT_TIMESTAMP(), HOUR),
        S.days_since_league_start,
        S.chaos_price_std_7d
    );