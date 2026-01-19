# 🏥 Wellbeing Healthcare Analytics Platform

A complete end-to-end AWS Data Analytics project for a fictional healthcare organization, built using Amazon S3, AWS Glue, Athena, and Amazon QuickSight.

This project delivers Appointments, Billing, and Lab Orders analytics dashboards with a secure, scalable, and production-ready architecture.

## 📌 Project Overview

The Wellbeing Healthcare Analytics Platform ingests raw CSV healthcare data, processes it using AWS Glue ETL jobs, models it into a star schema, and delivers interactive dashboards in Amazon QuickSight with Row-Level Security (RLS).

## 📂 Repository Structure

wellbeing-healthcare-analytics/
│
├── data/
│   ├── raw/
│   └── cleaned/
│
├── glue_jobs/
│   ├── clean_dim_date_job.py
│   ├── clean_dim_department_job.py
│   ├── clean_dim_doctor_job.py
│   ├── clean_dim_patient_job.py
│   ├── clean_fact_appointments_job.py
│   ├── clean_fact_billing_job.py
│   └── clean_fact_lab_orders_job.py
│
├── athena_queries/
│   ├── appointments_analysis.sql
│   ├── billing_analysis.sql
│   └── lab_orders_analysis.sql
│
├── rls/
│   ├── appointments_rls.csv
│   └── appointments_rls_manifest.json
│
├── docs/
│   ├── architecture_description.md
│   ├── data_model.md
│   ├── dashboard_kpis.md
│   └── rls_implementation.md
│
├── images/
│   ├── aws_healthcare_analytics_architecture.png
│   ├── appointments_data_model.png
│   ├── billings_data_model.png
│   └── lab_orders_data_model.png
│
└── README.md


## 🏗️ Architecture Overview

High-Level Flow
	1.	Source CSV files are ingested into Amazon S3 Raw Zone
	2.	AWS Glue Crawlers catalog raw data
	3.	AWS Glue ETL (PySpark) cleans, standardizes, and enriches data
	4.	Transformed data is stored in S3 Cleaned Zone (Parquet, Star Schema)
	5.	Cleaned data is cataloged in AWS Glue Data Catalog
	6.	Amazon Athena runs SQL queries on cleaned data
	7.	Amazon QuickSight loads data into SPICE and serves dashboards
	8.	Row-Level Security (RLS) restricts data visibility by role

## 🧱 Data Model (Star Schema)

### 📅 Appointments Data Model

### 💳 Billing Data Model

### 🧪 Lab Orders Data Model


## 📊 Dashboards

The platform includes three interactive dashboards built in Amazon QuickSight:

### 📅 Appointments Analytics Dashboard

KPIs & Insights
	•	Total Appointments
	•	Completed vs Cancelled vs No-Shows
	•	No-Show Rate (%)
	•	Appointments by Department
	•	No-Show Rate by Day of Week

🔗 Dashboard link:


### 💳 Billing Analytics Dashboard

KPIs & Insights
	•	Total Revenue
	•	Average Bill Amount
	•	Revenue by Department
	•	Revenue by Doctor
	•	Weekend vs Weekday Revenue

🔗 Dashboard link:

### 🧪 Lab Orders Analytics Dashboard

KPIs & Insights
	•	Total Lab Orders
	•	Orders by Test Type
	•	Orders by Department
	•	Orders Trend Over Time
	•	Patient-wise Lab Utilization

🔗 Dashboard link:

## 🔐 Row-Level Security (RLS)

Row-Level Security is implemented in Amazon QuickSight using an external RLS rules dataset stored in Amazon S3.

Roles & Access Rules

| Role             | Access Scope                                  |
|------------------|-----------------------------------------------|
| Admin            | Full access to all data                       |
| Department Head  | Access limited to assigned department         |
| Doctor           | Access limited to own records                 |
| Analyst          | Read-only access to all data                  |
| * (Wildcard)     | No restriction (matches all values)           |


RLS is enforced at the QuickSight dataset level, ensuring secure data access.

## 🛠️ Technologies Used

	•	Amazon S3 – Data lake storage
	•	AWS Glue – Crawlers, ETL, Data Catalog
	•	Amazon Athena – Serverless SQL analytics
	•	Amazon QuickSight – BI dashboards & SPICE
	•	PySpark – Data transformation
	•	Parquet – Optimized analytics storage

## 🚀 Key Highlights

	•	Production-grade lakehouse architecture
	•	Optimized Parquet + Star Schema
	•	Secure Row-Level Security (RLS)
	•	Scalable & serverless analytics
	•	End-to-end AWS-native solution

## 👤 Author

**Kaushik**  
Data Engineer | Analytics Engineer  
AWS • Glue • Athena • QuickSight • PySpark  

📧 Email: kaushik.p9699@gmail.com  
🌐 GitHub: https://github.com/Kaushik-Puttaswamy
📍 Location: India

## 📌 Disclaimer

This project is built for learning and portfolio purposes.
Wellbeing Healthcare is a fictional organization.



