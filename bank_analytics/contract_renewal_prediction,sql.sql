-- Query to identify factors that predict contract renewal
WITH contract_metrics AS (
    SELECT 
        c.contract_id,
        c.customer_id,
        c.product_id,
        c.end_date,
        -- Payment behavior
        COUNT(p.payment_id) AS total_payments,
        SUM(CASE WHEN p.payment_at <= p.due_date THEN 1 ELSE 0 END) AS on_time_payments,
        ROUND(AVG(CAST(p.payment_at AS DATE) - CAST(p.due_date AS DATE)), 1) AS avg_payment_delay,
        COUNT(cs.ticket_id) AS total_tickets,
        AVG(cs.satisfaction_score) AS avg_satisfaction,
        -- Renewal flag
        CASE WHEN c.renewal_contract_id IS NOT NULL THEN 1 ELSE 0 END AS renewed
    FROM contracts c
    LEFT JOIN payments p ON c.contract_id = p.contract_id
    LEFT JOIN customer_service cs ON c.contract_id = cs.contract_id
    WHERE c.end_date < CURRENT_DATE
      AND c.status = 'completed'
    GROUP BY c.contract_id, c.customer_id, c.product_id, c.end_date, c.renewal_contract_id
)
SELECT 
    -- Payment behavior brackets
    CASE 
        WHEN on_time_payments * 100.0 / NULLIF(total_payments, 0) >= 90 THEN '90-100%'
        WHEN on_time_payments * 100.0 / NULLIF(total_payments, 0) >= 75 THEN '75-89%'
        WHEN on_time_payments * 100.0 / NULLIF(total_payments, 0) >= 50 THEN '50-74%'
        ELSE 'Below 50%'
    END AS on_time_payment_bracket,
    -- Customer service satisfaction brackets
    CASE 
        WHEN avg_satisfaction >= 4.5 THEN 'Very Satisfied (4.5-5)'
        WHEN avg_satisfaction >= 3.5 THEN 'Satisfied (3.5-4.4)'
        WHEN avg_satisfaction >= 2.5 THEN 'Neutral (2.5-3.4)'
        WHEN avg_satisfaction > 0 THEN 'Unsatisfied (1-2.4)'
        ELSE 'No Feedback'
    END AS satisfaction_bracket,
    -- Customer service interaction brackets
    CASE 
        WHEN total_tickets = 0 THEN 'No Tickets'
        WHEN total_tickets = 1 THEN '1 Ticket'
        WHEN total_tickets = 2 THEN '2 Tickets'
        ELSE '3+ Tickets'
    END AS ticket_bracket,
    -- Metrics
    COUNT(*) AS contract_count,
    SUM(renewed) AS renewals,
    ROUND(SUM(renewed) * 100.0 / COUNT(*), 2) AS renewal_rate
FROM contract_metrics
GROUP BY on_time_payment_bracket, satisfaction_bracket, ticket_bracket
ORDER BY renewal_rate DESC;