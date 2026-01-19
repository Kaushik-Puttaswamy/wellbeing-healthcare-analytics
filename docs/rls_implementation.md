Row-Level Security (RLS) Implementation

This document describes the Row-Level Security (RLS) design, configuration, and enforcement approach used across the Wellbeing Healthcare Analytics Platform dashboards built in Amazon QuickSight.

RLS ensures that users only see data they are authorized to access, based on their organizational role and assigned attributes.

Dashboards covered:
	•	Appointments Analytics
	•	Billing Analytics
	•	Lab Orders Analytics

All RLS rules are centrally managed using CSV-based rule datasets stored in Amazon S3 and applied through Amazon QuickSight.

1. Purpose of Row-Level Security

Purpose:
Ensure secure, role-based data access while enabling a single shared dataset and dashboard for multiple user personas.

Key objectives:
	•	Protect patient and financial data
	•	Enforce least-privilege access
	•	Avoid dashboard duplication
	•	Simplify governance and auditability

2. RLS User Roles

The platform supports the following user roles:

| Role             | Description                                             |
|------------------|---------------------------------------------------------|
| Admin            | Full access to all records across all departments        |
| Department Head  | Access limited to assigned department                    |
| Doctor           | Access limited to their own records                      |
| Analyst          | Read-only access to assigned departments                 |

Each user is mapped to one role and one or more filter attributes.

3. RLS Rule Dataset

Purpose:
Define which rows of data each user is permitted to view.

Dataset Characteristics

| Attribute        | Value                                   |
|------------------|-----------------------------------------|
| Storage Location | Amazon S3                               |
| File Format      | CSV                                     |
| Header Row       | Yes                                     |
| Update Method    | Manual or automated pipeline            |
| Applied At       | Dataset level in Amazon QuickSight      |

The primary RLS rules file is stored in S3 and referenced by QuickSight during dataset refresh

4. RLS Rule Schema

The RLS rules dataset follows a consistent schema across all analytics domains.

Common Columns

| Column Name | Description                                                   |
|------------|---------------------------------------------------------------|
| user_name  | QuickSight user email or username                             |
| role       | User role (Admin, Department Head, Doctor, Analyst)           |
| department | Department name (nullable for Admin)                          |
| doctor_id  | Doctor identifier (nullable except for Doctor role)           |


5. Dataset-Level RLS Mapping

Purpose:
Link rule attributes to dataset columns.

Each curated fact table includes the following fields:
	•	department
	•	doctor_id

| user_name                     | role             | department   | doctor_id |
|-------------------------------|------------------|--------------|-----------|
| admin@wellbeing.com           | Admin            | ALL          | ALL       |
| cardio_head@wellbeing.com     | Department Head  | Cardiology   | ALL       |
| dr_smith@wellbeing.com        | Doctor           | Cardiology   | D1001     |
| analyst_ops@wellbeing.com     | Analyst          | Radiology   | ALL       |

The RLS dataset is attached to:
	•	Appointments fact dataset
	•	Billing fact dataset
	•	Lab Orders fact dataset

| Role            | Enforcement Rule                         |
|-----------------|------------------------------------------|
| Admin           | No filters applied                       |
| Department Head | department = rules.department            |
| Doctor          | doctor_id = rules.doctor_id              |
| Analyst         | department IN assigned departments       |


    6. Dashboard Behavior with RLS

Purpose:
Ensure dashboards dynamically adapt to logged-in users.

User Experience
	•	Users see only authorized KPIs
	•	Visuals automatically recalculate metrics
	•	Drill-downs respect RLS boundaries
	•	No empty or broken visuals

Example Scenarios

| User            | Visible Data                              |
|-----------------|-------------------------------------------|
| Admin           | All hospitals, departments, doctors       |
| Department Head | Only their department                    |
| Doctor          | Only their own patients and activity     |
| Analyst         | Assigned departments only                |


7. RLS Maintenance & Governance

Update Process
	•	RLS CSV files are updated in Amazon S3
	•	QuickSight datasets refresh automatically
	•	No dashboard republishing required

Best Practices
	•	One RLS dataset per domain (Appointments, Billing, Labs)
	•	Validate user-role mappings before refresh
	•	Restrict S3 write access to data governance team
	•	Log changes for audit purposes

⸻

8. Security & Compliance Considerations
	•	Enforces HIPAA-aligned access principles
	•	Prevents cross-department data leakage
	•	Centralized rule management
	•	Fully compatible with SPICE acceleration

⸻

9. Performance Impact
	•	RLS filters are applied before SPICE ingestion
	•	No runtime performance degradation
	•	Supports thousands of users per dataset
	•	Optimized for star-schema fact tables

⸻

10. Summary

The Row-Level Security framework enables:
	•	Secure multi-tenant dashboards
	•	Role-aware analytics
	•	Scalable governance
	•	Simplified operational management

This design allows the Wellbeing Healthcare Analytics Platform to maintain a single version of truth while ensuring strict data access controls.

⸻

Author: Wellbeing Healthcare Analytics Team
Last Updated: January 2026