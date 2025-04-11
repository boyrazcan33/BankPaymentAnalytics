-- Query to identify the total count and amount of payments that were paid later than due date
SELECT 
    COUNT(*) AS total_late_payments,
    SUM(paid_amount) AS total_late_amount,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM payments WHERE status != 'scheduled'), 2) AS late_payment_percentage,
    ROUND(AVG(payment_at - due_date), 1) AS avg_days_late
FROM payments
WHERE payment_at > due_date
  AND status = 'late';