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

![Wellbeing Healthcare Analytics Architecture](https://github.com/Kaushik-Puttaswamy/wellbeing-healthcare-analytics/blob/main/architecture/aws_healthcare_analytics_architecture.png.png)

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

![appointments_data_model](https://github.com/Kaushik-Puttaswamy/wellbeing-healthcare-analytics/blob/main/data%20model/appointments_data_model.png)

### 💳 Billing Data Model

![billings_data_model](https://github.com/Kaushik-Puttaswamy/wellbeing-healthcare-analytics/blob/main/data%20model/billings_data_model.png)

### 🧪 Lab Orders Data Model

![lab_orders_data_model](https://github.com/Kaushik-Puttaswamy/wellbeing-healthcare-analytics/blob/main/data%20model/lab_orders_data_model.png)

## 📊 Dashboards

The platform includes three interactive dashboards built in Amazon QuickSight:

### 📅 Appointments Analytics Dashboard

KPIs & Insights
	•	Total Appointments
	•	Completed vs Cancelled vs No-Shows
	•	No-Show Rate (%)
	•	Appointments by Department
	•	No-Show Rate by Day of Week

🔗 Dashboard link: https://ap-south-1.quicksight.aws.amazon.com/sn/account/kaush-quicksight-project/dashboards/c3485f3f-850b-46ab-8dc2-3e2ea4321a4a

![appointments_dashboard](https://github.com/Kaushik-Puttaswamy/wellbeing-healthcare-analytics/blob/main/appointments_dashboard.png)


### 💳 Billing Analytics Dashboard

KPIs & Insights
	•	Total Revenue
	•	Average Bill Amount
	•	Revenue by Department
	•	Revenue by Doctor
	•	Weekend vs Weekday Revenue

🔗 Dashboard link: https://ap-south-1.quicksight.aws.amazon.com/sn/account/kaush-quicksight-project/dashboards/af0335c5-544f-4480-b82c-3482d8afba4c

![billing_dashboard](https://github.com/Kaushik-Puttaswamy/wellbeing-healthcare-analytics/blob/main/billing_dashboard.png)


### 🧪 Lab Orders Analytics Dashboard

KPIs & Insights
	•	Total Lab Orders
	•	Orders by Test Type
	•	Orders by Department
	•	Orders Trend Over Time
	•	Patient-wise Lab Utilization

🔗 Dashboard link: https://ap-south-1.quicksight.aws.amazon.com/sn/account/kaush-quicksight-project/dashboards/023a24a0-6dfa-44b7-884a-075562d89a2f

![lab_orders_dashboard](https://github.com/Kaushik-Puttaswamy/wellbeing-healthcare-analytics/blob/main/lab_orders_dashboard.png)


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



