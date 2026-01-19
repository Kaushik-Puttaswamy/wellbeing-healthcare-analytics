import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.sql.functions import (
    col,
    sequence,
    explode,
    to_date,
    date_format,
    year,
    month,
    dayofmonth,
    weekofyear,
    dayofweek,
    when
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
# GENERATE DATE RANGE (FACT-SAFE RANGE)
# --------------------------------------------------
# Covers all fact tables: appointments, billing, lab_orders
date_range_df = spark.sql("""
SELECT explode(
    sequence(
        to_date('2023-01-01'),
        to_date('2025-12-31'),
        interval 1 day
    )
) AS full_date
""")

# --------------------------------------------------
# BUILD DATE DIMENSION
# --------------------------------------------------
clean_df = (
    date_range_df
    .withColumn("date_id", date_format(col("full_date"), "yyyyMMdd").cast("int"))
    .withColumn("year", year(col("full_date")))
    .withColumn("month", month(col("full_date")))
    .withColumn("day", dayofmonth(col("full_date")))
    .withColumn("month_name", date_format(col("full_date"), "MMMM"))
    .withColumn("day_name", date_format(col("full_date"), "EEEE"))
    .withColumn("week_of_year", weekofyear(col("full_date")))
    .withColumn(
        "is_weekend",
        when(dayofweek(col("full_date")).isin(1, 7), "Yes").otherwise("No")
    )
)

# --------------------------------------------------
# WRITE CLEANED DATE DIMENSION
# --------------------------------------------------
clean_df.write \
    .mode("overwrite") \
    .format("parquet") \
    .save("s3://wellbeing-healthcare-datalake/cleaned/dim_date/")

job.commit()