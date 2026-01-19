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
    regexp_replace,
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
# READ RAW DATA FROM GLUE CATALOG
# --------------------------------------------------
raw_df = glueContext.create_dynamic_frame.from_catalog(
    database="wellbeing_raw_db",
    table_name="dim_doctor_csv"
).toDF()

# --------------------------------------------------
# DATA CLEANING & STANDARDIZATION
# --------------------------------------------------
clean_df = (
    raw_df

    # -----------------------------
    # doctor_id
    # -----------------------------
    .withColumn("doctor_id", col("doctor_id").cast("int"))
    .filter(col("doctor_id").isNotNull())

    # -----------------------------
    # doctor_name (STRICT BUSINESS RULE)
    # Only 2 doctors exist:
    # - Dr Jones
    # - Dr Smith
    # -----------------------------
    .withColumn(
        "doctor_name",
        when(upper(col("doctor_name")).like("%JONES%"), "Dr Jones")
        .when(upper(col("doctor_name")).like("%SMITH%"), "Dr Smith")
        .otherwise("Unknown")
    )

    # -----------------------------
    # department_id
    # -----------------------------
    .withColumn("department_id", col("department_id").cast("int"))
    .filter(col("department_id").isNotNull())

    # -----------------------------
    # joining_date (multiple formats)
    # -----------------------------
    .withColumn(
        "joining_date",
        coalesce(
            to_date(col("joining_date"), "yyyy-MM-dd"),
            to_date(col("joining_date"), "dd/MM/yyyy"),
            to_date(col("joining_date"), "yyyyMMdd")
        )
    )
)

# --------------------------------------------------
# WRITE CLEANED DATA TO S3 (PARQUET)
# --------------------------------------------------
clean_df.write \
    .mode("overwrite") \
    .format("parquet") \
    .save("s3://wellbeing-healthcare-datalake/cleaned/dim_doctor/")

# --------------------------------------------------
# COMMIT JOB
# --------------------------------------------------
job.commit()