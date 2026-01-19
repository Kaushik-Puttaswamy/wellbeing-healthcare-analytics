import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.sql.functions import (
    col,
    abs,
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
# READ RAW BILLING DATA
# --------------------------------------------------
raw_df = glueContext.create_dynamic_frame.from_catalog(
    database="wellbeing_raw_db",
    table_name="fact_billing_csv"
).toDF()

# --------------------------------------------------
# DATA CLEANING LOGIC
# --------------------------------------------------
clean_df = (
    raw_df

    # Cast IDs
    .withColumn("bill_id", col("bill_id").cast("int"))
    .withColumn("patient_id", col("patient_id").cast("int"))
    .withColumn("doctor_id", col("doctor_id").cast("int"))

    # Filter invalid IDs
    .filter(col("bill_id").isNotNull())
    .filter(col("patient_id").isNotNull())
    .filter(col("doctor_id").isNotNull())

    # Fix negative amount entry errors
    .withColumn("amount", abs(col("amount").cast("int")))
    .filter(col("amount") > 0)

    # Parse bill_date (ALL supported formats)
    .withColumn(
        "bill_date",
        coalesce(
            to_date(col("bill_date"), "yyyy-MM-dd"),
            to_date(col("bill_date"), "dd-MM-yyyy"),
            to_date(col("bill_date"), "yyyyMMdd"),
            to_date(col("bill_date"), "yyyy/MM/dd")
        )
    )
    .filter(col("bill_date").isNotNull())

    # Final schema
    .select(
        "bill_id",
        "patient_id",
        "doctor_id",
        "amount",
        "bill_date"
    )
)

# --------------------------------------------------
# WRITE CLEANED BILLING DATA
# --------------------------------------------------
clean_df.write \
    .mode("overwrite") \
    .format("parquet") \
    .save("s3://wellbeing-healthcare-datalake/cleaned/fact_billing/")

job.commit()