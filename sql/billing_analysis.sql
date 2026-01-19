-- ==========================
-- Billing Analytics Queries
-- ==========================

-- 1. Total Revenue
SELECT
    SUM(amount) AS total_revenue
FROM wellbeing_cleaned_db.clean_fact_billing;

-- 2. Total Bills
SELECT
    COUNT(bill_id) AS total_bills
FROM wellbeing_cleaned_db.clean_fact_billing;

-- 3. Average Bill Amount
SELECT
    ROUND(AVG(amount), 2) AS avg_bill_amount
FROM wellbeing_cleaned_db.clean_fact_billing;
-- 4. Revenue by Department
SELECT
    d.department_name,
    SUM(b.amount) AS revenue
FROM wellbeing_cleaned_db.clean_fact_billing b
JOIN wellbeing_cleaned_db.clean_dim_department d
    ON b.department_id = d.department_id
GROUP BY d.department_name
ORDER BY revenue DESC;
-- 5. Revenue by Doctor
SELECT
    doc.doctor_name,
    SUM(b.amount) AS revenue
FROM wellbeing_cleaned_db.clean_fact_billing b
JOIN wellbeing_cleaned_db.clean_dim_doctor doc
    ON b.doctor_id = doc.doctor_id
GROUP BY doc.doctor_name
ORDER BY revenue DESC;

-- 6. Revenue Trend Over Time (Monthly)
SELECT
    dd.year,
    dd.month,
    SUM(b.amount) AS monthly_revenue
FROM wellbeing_cleaned_db.clean_fact_billing b
JOIN wellbeing_cleaned_db.clean_dim_date dd
    ON b.bill_date = dd.full_date
GROUP BY dd.year, dd.month
ORDER BY dd.year, dd.month;
-- 7. Weekend vs Weekday Revenue
SELECT
    dd.is_weekend,
    SUM(b.amount) AS revenue
FROM wellbeing_cleaned_db.clean_fact_billing b
JOIN wellbeing_cleaned_db.clean_dim_date dd
    ON b.bill_date = dd.full_date
GROUP BY dd.is_weekend;