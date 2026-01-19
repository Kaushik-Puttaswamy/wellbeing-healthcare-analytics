import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.sql.functions import col, trim, initcap

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
# READ RAW DEPARTMENT DATA FROM GLUE CATALOG
# --------------------------------------------------
raw_df = glueContext.create_dynamic_frame.from_catalog(
    database="wellbeing_raw_db",
    table_name="dim_department_csv"
).toDF()

# --------------------------------------------------
# DATA CLEANING LOGIC
# --------------------------------------------------
clean_df = (
    raw_df
    .withColumn("department_id", col("department_id").cast("int"))
    .filter(col("department_id").isNotNull())
    .withColumn("department_name", initcap(trim(col("department_name"))))
)

# --------------------------------------------------
# WRITE CLEANED DATA TO S3
# --------------------------------------------------
clean_df.write \
    .mode("overwrite") \
    .format("parquet") \
    .save("s3://wellbeing-healthcare-datalake/cleaned/dim_department/")

job.commit()