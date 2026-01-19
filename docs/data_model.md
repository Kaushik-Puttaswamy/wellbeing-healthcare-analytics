# Data Model – Wellbeing Healthcare Analytics Platform

This document describes the **logical and physical data model** used in the Wellbeing Healthcare Analytics Platform.  
The platform follows a **star schema design** optimized for analytics and reporting in Amazon Athena and Amazon QuickSight.

---

## 🧩 Overview

- **Fact tables** store transactional healthcare data
- **Dimension tables** store descriptive attributes
- Data is stored in **Amazon S3 (Cleaned Zone)** in **Parquet format**
- Schemas are managed via **AWS Glue Data Catalog**
- Used by **Athena** and **QuickSight (SPICE)**

---

## ⭐ Fact Tables

---

### 📌 fact_appointments

Stores appointment-level transactional data.

| Column            | Description                                   |
|------------------|-----------------------------------------------|
| appointment_id   | Unique appointment identifier                 |
| patient_id       | Foreign key to dim_patient                    |
| doctor_id        | Foreign key to dim_doctor                     |
| department_id    | Foreign key to dim_department                 |
| date_id          | Foreign key to dim_date                       |
| status           | Appointment status (Completed, Cancelled, No Show) |
| service_date     | Appointment date                              |
| is_weekend       | Weekend flag (Yes / No)                       |

---

### 📌 fact_billing

Stores billing and revenue-related data.

| Column         | Description                                   |
|---------------|-----------------------------------------------|
| bill_id       | Unique billing identifier                     |
| patient_id    | Foreign key to dim_patient                    |
| doctor_id     | Foreign key to dim_doctor                     |
| department_id | Foreign key to dim_department                 |
| date_id       | Foreign key to dim_date                       |
| bill_date     | Billing date                                  |
| amount        | Billed amount                                 |

---

### 📌 fact_lab_orders

Stores laboratory test orders.

| Column         | Description                                   |
|---------------|-----------------------------------------------|
| lab_order_id  | Unique lab order identifier                   |
| patient_id    | Foreign key to dim_patient                    |
| department_id | Foreign key to dim_department                 |
| date_id       | Foreign key to dim_date                       |
| test_name     | Name of lab test                              |
| result_value  | Test result value                             |
| order_date    | Lab order date                                |

---

## 📚 Dimension Tables

---

### 📘 dim_patient

Stores patient demographic information.

| Column        | Description                |
|--------------|----------------------------|
| patient_id   | Unique patient identifier  |
| patient_name | Patient full name          |
| gender       | Patient gender             |
| dob          | Date of birth              |
| city         | Patient city               |

---

### 📘 dim_doctor

Stores doctor details.

| Column        | Description                |
|--------------|----------------------------|
| doctor_id    | Unique doctor identifier   |
| doctor_name  | Doctor full name           |
| department_id| Foreign key to department  |
| joining_date | Doctor joining date        |

---

### 📘 dim_department

Stores hospital department information.

| Column          | Description                    |
|-----------------|--------------------------------|
| department_id   | Unique department identifier   |
| department_name | Department name                |

---

### 📘 dim_date

Stores date-related attributes for time-based analysis.

| Column        | Description                     |
|--------------|---------------------------------|
| date_id      | Unique date identifier          |
| full_date    | Calendar date                   |
| year         | Year                            |
| month        | Month number                    |
| month_name   | Month name                      |
| day          | Day of month                    |
| day_name     | Day name                        |
| week_of_year | Week number                     |
| is_weekend   | Weekend flag (Yes / No)         |

---

## 🔗 Relationships (Star Schema)

- All **fact tables** join to:
  - `dim_patient` via `patient_id`
  - `dim_department` via `department_id`
  - `dim_date` via `date_id`
- `fact_appointments` and `fact_billing` also join to:
  - `dim_doctor` via `doctor_id`

This design ensures:
- Fast aggregation queries
- Optimized SPICE ingestion
- Clear dimensional slicing in dashboards

---

## ✅ Usage

- Queried using **Amazon Athena**
- Visualized in **Amazon QuickSight**
- Secured using **Row-Level Security (RLS)** based on:
  - Department
  - Doctor
  - User role

---

## 📌 Notes

- All tables are stored in **Parquet format**
- Partitioning is applied on date fields where applicable
- Schema evolution handled via AWS Glue Data Catalog

---

_End of Data Model Documentation_