-- Query to analyze the distribution of payment statuses
SELECT 
    status,
    COUNT(*) AS payment_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM payments), 2) AS percentage,
    SUM(scheduled_amount) AS total_scheduled,
    SUM(paid_amount) AS total_paid,
    ROUND(SUM(paid_amount) * 100.0 / NULLIF(SUM(scheduled_amount), 0), 2) AS collection_rate
FROM payments
GROUP BY status
ORDER BY payment_count DESC;