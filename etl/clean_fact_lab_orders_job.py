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
# READ RAW LAB ORDERS DATA
# --------------------------------------------------
raw_df = glueContext.create_dynamic_frame.from_catalog(
    database="wellbeing_raw_db",
    table_name="fact_lab_orders_csv"
).toDF()

# --------------------------------------------------
# DATA CLEANING LOGIC
# --------------------------------------------------
clean_df = (
    raw_df

    # Cast IDs
    .withColumn("lab_order_id", col("lab_order_id").cast("int"))
    .withColumn("patient_id", col("patient_id").cast("int"))
    .withColumn("department_id", col("department_id").cast("int"))

    # Filter invalid IDs
    .filter(col("lab_order_id").isNotNull())
    .filter(col("patient_id").isNotNull())
    .filter(col("department_id").isNotNull())

    # Enforce controlled vocabulary for test_name
    .withColumn(
        "test_name",
        when(upper(trim(col("test_name"))) == "MRI", "MRI")
        .when(upper(trim(col("test_name"))) == "CT SCAN", "CT Scan")
        .when(upper(trim(col("test_name"))) == "X-RAY", "X-Ray")
        .when(upper(trim(col("test_name"))) == "BLOOD TEST", "Blood Test")
        .otherwise("Unknown")
    )

    # Normalize result_value
    .withColumn(
        "result_value",
        when(upper(trim(col("result_value"))) == "NORMAL", "Normal")
        .when(upper(trim(col("result_value"))) == "POSITIVE", "Positive")
        .when(upper(trim(col("result_value"))) == "NEGATIVE", "Negative")
        .otherwise("Unknown")
    )

    # Parse order_date (all supported formats)
    .withColumn(
        "order_date",
        coalesce(
            to_date(col("order_date"), "yyyy-MM-dd"),
            to_date(col("order_date"), "yyyyMMdd"),
            to_date(col("order_date"), "dd.MM.yyyy")
        )
    )
    .filter(col("order_date").isNotNull())

    # Optional: drop unknowns
    .filter(col("test_name") != "Unknown")
    .filter(col("result_value") != "Unknown")

    # Final schema
    .select(
        "lab_order_id",
        "patient_id",
        "department_id",
        "test_name",
        "result_value",
        "order_date"
    )
)

# --------------------------------------------------
# WRITE CLEANED LAB ORDERS DATA
# --------------------------------------------------
clean_df.write \
    .mode("overwrite") \
    .format("parquet") \
    .save("s3://wellbeing-healthcare-datalake/cleaned/fact_lab_orders/")

job.commit()