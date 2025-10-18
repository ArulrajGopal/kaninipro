from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType
from pyspark.sql.functions import col
import os

spark = (
    SparkSession.builder.appName("people_delta")
    .getOrCreate()
)

account_key = os.getenv("AZURE_STORAGE_KEY")
spark.conf.set("fs.azure.account.key.arulrajgopalshare.dfs.core.windows.net",account_key)
spark.conf.set("spark.sql.adaptive.enabled", "false")
spark.conf.set("spark.sql.shuffle.partitions", 10)

schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("first_name", StringType(), True),
    StructField("middle_name", StringType(), True),
    StructField("last_name", StringType(), True),
    StructField("gender", StringType(), True),
    StructField("birth_dt", TimestampType(), True),
    StructField("ssn", StringType(), True),
    StructField("salary", IntegerType(), True),
    StructField("city", StringType(), True)
])

people_df = spark.read.format("csv")\
    .schema(schema) \
    .load("abfss://kaniniwitharul@arulrajgopalshare.dfs.core.windows.net/people/people_csv/people.csv")


age_derived_and_filtered_df = people_df.selectExpr("*","floor(months_between(current_date(), birth_dt) / 12) as age")\
                                .filter(col("salary")> 30000)

aggregated_df = age_derived_and_filtered_df.groupBy("city").count()

aggregated_df.write.mode("overwrite").format("delta")\
                .save("abfss://kaniniwitharul@arulrajgopalshare.dfs.core.windows.net/test_path/people_delta")

