

WITH daily_stats AS (
    SELECT 
        toDate(timeStamp) AS metric_date,
        COUNT(hash) AS total_transactions,
        SUM(value) AS total_volume_usdt,
        COUNT(DISTINCT from_address) AS unique_active_senders
    FROM web3_dwh.stg_usdt_transfers
    GROUP BY metric_date
)
SELECT 
    metric_date,
    total_transactions,
    total_volume_usdt,
    unique_active_senders,
    lagInFrame(total_volume_usdt, 1) OVER (ORDER BY metric_date) AS prev_day_volume,
    ROUND((total_volume_usdt - lagInFrame(total_volume_usdt, 1) OVER (ORDER BY metric_date)) 
          / NULLIF(lagInFrame(total_volume_usdt, 1) OVER (ORDER BY metric_date), 0) * 100, 2) AS dod_growth_pct
FROM daily_stats
ORDER BY metric_date DESC