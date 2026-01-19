-- ==============================
-- Appointments Analytics Queries
-- ==============================

-- 1. Total Appointments
SELECT COUNT(*) AS total_appointments
FROM wellbeing_cleaned_db.clean_fact_appointments;

-- 2. Appointments by Status
SELECT
    status,
    COUNT(*) AS appointment_count
FROM wellbeing_cleaned_db.clean_fact_appointments
GROUP BY status
ORDER BY appointment_count DESC;

-- 3. Completed vs Cancelled vs No-Show Rate
SELECT
    status,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage
FROM wellbeing_cleaned_db.clean_fact_appointments
GROUP BY status;
-- 4. Appointments by Department
SELECT
    d.department_name,
    COUNT(a.appointment_id) AS total_appointments
FROM wellbeing_cleaned_db.clean_fact_appointments a
JOIN wellbeing_cleaned_db.clean_dim_department d
    ON a.department_id = d.department_id
GROUP BY d.department_name
ORDER BY total_appointments DESC;

-- 5. Appointments by Doctor
SELECT
    doc.doctor_name,
    COUNT(a.appointment_id) AS appointment_count
FROM wellbeing_cleaned_db.clean_fact_appointments a
JOIN wellbeing_cleaned_db.clean_dim_doctor doc
    ON a.doctor_id = doc.doctor_id
GROUP BY doc.doctor_name
ORDER BY appointment_count DESC;

-- 6. No-Show Rate by Day of Week
SELECT
    dd.day_name,
    ROUND(
        SUM(CASE WHEN a.status = 'No Show' THEN 1 ELSE 0 END) * 100.0
        / COUNT(*),
        2
    ) AS no_show_rate
FROM wellbeing_cleaned_db.clean_fact_appointments a
JOIN wellbeing_cleaned_db.clean_dim_date dd
    ON a.service_date = dd.full_date
GROUP BY dd.day_name
ORDER BY no_show_rate DESC;