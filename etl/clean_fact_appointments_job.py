import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.sql.functions import (
    col,
    trim,
    upper,
    when,
    coalesce,
    to_date
)

# --------------------------------------------------
# JOB INITIALIZATION
# --------------------------------------------------
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# --------------------------------------------------
# READ RAW APPOINTMENTS DATA
# --------------------------------------------------
raw_df = glueContext.create_dynamic_frame.from_catalog(
    database="wellbeing_raw_db",
    table_name="fact_appointments_csv"
).toDF()

# --------------------------------------------------
# DATA CLEANING LOGIC
# --------------------------------------------------
clean_df = (
    raw_df

    # Cast IDs
    .withColumn("appointment_id", col("appointment_id").cast("int"))
    .withColumn("patient_id", col("patient_id").cast("int"))
    .withColumn("doctor_id", col("doctor_id").cast("int"))

    # Filter invalid IDs
    .filter(col("appointment_id").isNotNull())
    .filter(col("patient_id").isNotNull())
    .filter(col("doctor_id").isNotNull())

    # Parse service_date
    .withColumn(
        "service_date",
        coalesce(
            to_date(col("service_date"), "yyyy-MM-dd"),
            to_date(col("service_date"), "dd-MM-yyyy"),
            to_date(col("service_date"), "yyyyMMdd")
        )
    )
    .filter(col("service_date").isNotNull())

    # Normalize status
    .withColumn(
        "status",
        when(upper(trim(col("status"))) == "COMPLETED", "Completed")
        .when(upper(trim(col("status"))) == "CANCELLED", "Cancelled")
        .when(upper(trim(col("status"))) == "NO SHOW", "No Show")
        .otherwise("Unknown")
    )

    # Optional: keep only valid statuses
    .filter(col("status") != "Unknown")

    # Select final schema
    .select(
        "appointment_id",
        "patient_id",
        "doctor_id",
        "service_date",
        "status"
    )
)

# --------------------------------------------------
# WRITE CLEANED FACT DATA
# --------------------------------------------------
clean_df.write \
    .mode("overwrite") \
    .format("parquet") \
    .save("s3://wellbeing-healthcare-datalake/cleaned/fact_appointments/")

job.commit()