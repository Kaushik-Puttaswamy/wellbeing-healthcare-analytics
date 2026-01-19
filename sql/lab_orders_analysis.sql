-- ============================
-- Lab Orders Analytics Queries
-- ============================

-- 1. Total Lab Orders
SELECT
    COUNT(lab_order_id) AS total_lab_orders
FROM wellbeing_cleaned_db.clean_fact_lab_orders;

-- 2. Lab Orders by Test Type
SELECT
    test_name,
    COUNT(lab_order_id) AS test_count
FROM wellbeing_cleaned_db.clean_fact_lab_orders
GROUP BY test_name
ORDER BY test_count DESC;

-- 3. Lab Orders by Department
SELECT
    d.department_name,
    COUNT(l.lab_order_id) AS lab_orders
FROM wellbeing_cleaned_db.clean_fact_lab_orders l
JOIN wellbeing_cleaned_db.clean_dim_department d
    ON l.department_id = d.department_id
GROUP BY d.department_name
ORDER BY lab_orders DESC;

-- 4. Lab Orders Trend Over Time (Monthly)
SELECT
    dd.year,
    dd.month,
    COUNT(l.lab_order_id) AS lab_orders
FROM wellbeing_cleaned_db.clean_fact_lab_orders l
JOIN wellbeing_cleaned_db.clean_dim_date dd
    ON l.order_date = dd.full_date
GROUP BY dd.year, dd.month
ORDER BY dd.year, dd.month;

-- 5. Lab Orders by Patient Gender
SELECT
    p.gender,
    COUNT(l.lab_order_id) AS lab_orders
FROM wellbeing_cleaned_db.clean_fact_lab_orders l
JOIN wellbeing_cleaned_db.clean_dim_patient p
    ON l.patient_id = p.patient_id
GROUP BY p.gender;

-- 6. Weekend vs Weekday Lab Orders
SELECT
    dd.is_weekend,
    COUNT(l.lab_order_id) AS lab_orders
FROM wellbeing_cleaned_db.clean_fact_lab_orders l
JOIN wellbeing_cleaned_db.clean_dim_date dd
    ON l.order_date = dd.full_date
GROUP BY dd.is_weekend;