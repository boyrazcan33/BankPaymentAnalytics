-- Query to analyze performance by product type
SELECT 
    p.category AS product_category,
    COUNT(DISTINCT c.contract_id) AS total_contracts,
    COUNT(DISTINCT c.customer_id) AS unique_customers,
    ROUND(AVG(c.amount), 2) AS avg_contract_amount,
    ROUND(AVG(c.interest_rate), 2) AS avg_interest_rate,
    -- Payment metrics
    COUNT(pm.payment_id) AS total_payments,
    ROUND(SUM(pm.paid_amount), 2) AS total_paid_amount,
    ROUND(SUM(pm.interest_amount), 2) AS total_interest_earned,
    ROUND(SUM(pm.fee_amount), 2) AS total_fees_collected,
    -- Payment behavior
    ROUND(SUM(CASE WHEN pm.payment_at <= pm.due_date AND pm.status = 'completed' THEN 1 ELSE 0 END) * 100.0 / 
          NULLIF(SUM(CASE WHEN pm.status != 'scheduled' THEN 1 ELSE 0 END), 0), 2) AS on_time_payment_percentage,
		 ROUND(AVG(COALESCE(pm.payment_at, CURRENT_DATE) - pm.due_date), 2) AS avg_days_from_scheduled_date

		  

FROM products p
JOIN contracts c ON p.product_id = c.product_id
LEFT JOIN payments pm ON c.contract_id = pm.contract_id
WHERE pm.status != 'scheduled' OR pm.status IS NULL -- Exclude scheduled payments or include contracts with no payments
GROUP BY p.category
ORDER BY on_time_payment_percentage DESC;