-- Query to analyze customer acquisition and retention by channel
WITH acquisition_metrics AS (
    SELECT
        acquisition_channel,
        DATE_TRUNC('month', signup_date) AS acquisition_month,
        COUNT(*) AS new_customers,
        AVG(acquisition_cost) AS avg_acquisition_cost
    FROM customers
    GROUP BY acquisition_channel, DATE_TRUNC('month', signup_date)
),
retention_metrics AS (
    SELECT
        c.acquisition_channel,
        DATE_TRUNC('month', c.signup_date) AS acquisition_month,
        COUNT(DISTINCT c.customer_id) AS original_customers,
        COUNT(DISTINCT CASE WHEN ct.start_date >= c.signup_date + INTERVAL '3 months' 
                          THEN c.customer_id END) AS retained_after_3m,
        COUNT(DISTINCT CASE WHEN ct.start_date >= c.signup_date + INTERVAL '6 months' 
                          THEN c.customer_id END) AS retained_after_6m,
        COUNT(DISTINCT CASE WHEN ct.start_date >= c.signup_date + INTERVAL '12 months' 
                          THEN c.customer_id END) AS retained_after_12m
    FROM customers c
    LEFT JOIN contracts ct ON c.customer_id = ct.customer_id
    WHERE c.signup_date <= CURRENT_DATE - INTERVAL '12 months'
    GROUP BY c.acquisition_channel, DATE_TRUNC('month', c.signup_date)
)
SELECT
    a.acquisition_channel,
    a.acquisition_month,
    a.new_customers,
    a.avg_acquisition_cost,
    r.original_customers,
    r.retained_after_3m,
    r.retained_after_6m,
    r.retained_after_12m,
    ROUND(r.retained_after_3m * 100.0 / NULLIF(r.original_customers, 0), 2) AS retention_rate_3m,
    ROUND(r.retained_after_6m * 100.0 / NULLIF(r.original_customers, 0), 2) AS retention_rate_6m,
    ROUND(r.retained_after_12m * 100.0 / NULLIF(r.original_customers, 0), 2) AS retention_rate_12m
FROM acquisition_metrics a
JOIN retention_metrics r ON a.acquisition_channel = r.acquisition_channel 
                        AND a.acquisition_month = r.acquisition_month
ORDER BY a.acquisition_month DESC, retention_rate_12m DESC;