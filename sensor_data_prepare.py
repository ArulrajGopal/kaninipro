from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType
from pyspark.sql.functions import expr, rand, substring, lit, current_timestamp, col, date_format, add_months, current_date, trunc,  last_day
from datetime import datetime
import os

spark = (
    SparkSession.builder.appName("people_delta")
    .getOrCreate()
)

# account_key = os.getenv("AZURE_STORAGE_KEY")
account_key = ''
spark.conf.set("fs.azure.account.key.kaniniproraw.dfs.core.windows.net",account_key)

for i in range(6000):
    loaded_dt = datetime.now().strftime("%Y%m%d%H%M%S")
    vehcile_id_df = spark.range(1, 10000001).withColumnRenamed("id", "vehicle_id")

    final_df = vehcile_id_df\
                        .withColumn("unit_id",(rand() * 50000).cast("int") + 1)\
                        .withColumn("sensor_a",(rand() * 1000).cast("int") + 1)\
                        .withColumn("sensor_b",(rand() * 1000).cast("int") + 1)\
                        .withColumn("sensor_c",(rand() * 1000).cast("int") + 1)\
                        .withColumn("sensor_d",(rand() * 1000).cast("int") + 1)\
                        .withColumn("sensor_e",(rand() * 1000).cast("int") + 1)\
                        .withColumn("sensor_f",(rand() * 1000).cast("int") + 1)\
                        .withColumn("sensor_g",(rand() * 1000).cast("int") + 1)\
                        .withColumn("sensor_h",(rand() * 1000).cast("int") + 1)\
                        .withColumn("loaded_dt", lit(loaded_dt))


    final_df.write.mode("append").partitionBy("loaded_dt").format("delta")\
                        .save("abfss://data@kaniniproraw.dfs.core.windows.net/test_data/sensor_data")
        

     

