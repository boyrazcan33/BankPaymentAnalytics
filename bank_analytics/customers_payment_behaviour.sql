-- Query to segment customers by payment behavior
WITH customer_payment_stats AS (
    SELECT 
        c.customer_id,
        c.name,
        c.risk_score,
        COUNT(p.payment_id) AS total_payments,
        SUM(CASE WHEN p.payment_at <= p.due_date THEN 1 ELSE 0 END) AS on_time_payments,
        SUM(CASE WHEN p.payment_at > p.due_date THEN 1 ELSE 0 END) AS late_payments,
        ROUND(AVG(COALESCE(p.payment_at, CURRENT_DATE) - p.due_date), 2) AS avg_days_from_due_date

    FROM customers c
    LEFT JOIN contracts ct ON c.customer_id = ct.customer_id
    LEFT JOIN payments p ON ct.contract_id = p.contract_id
    WHERE p.status != 'scheduled' -- Exclude scheduled payments for accurate behavior analysis
    GROUP BY c.customer_id, c.name, c.risk_score
)
SELECT 
    customer_id,
    name,
    risk_score,
    total_payments,
    on_time_payments,
    late_payments,
    ROUND(on_time_payments * 100.0 / NULLIF(total_payments, 0), 2) AS on_time_percentage,
    avg_days_from_due_date,
    CASE 
        WHEN total_payments = 0 THEN 'New Customer'
        WHEN on_time_payments * 100.0 / total_payments >= 95 THEN 'Excellent Payer'
        WHEN on_time_payments * 100.0 / total_payments >= 80 THEN 'Good Payer'
        WHEN on_time_payments * 100.0 / total_payments >= 60 THEN 'Average Payer'
        ELSE 'At Risk'
    END AS payment_segment
FROM customer_payment_stats
ORDER BY CASE 
    WHEN total_payments = 0 THEN 0 
    ELSE ROUND(on_time_payments * 100.0 / NULLIF(total_payments, 0), 2) 
END DESC;
