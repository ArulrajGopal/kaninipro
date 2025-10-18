from pyspark.sql import SparkSession
from datetime import datetime



def log_message(log_message):
    spark = SparkSession.getActiveSession()
    
    spark.createDataFrame([(str(datetime.now()), log_message)])\
        .write.mode("append")\
        .format("parquet")\
        .save("abfss://kaniniwitharul@arulrajgopalshare.dfs.core.windows.net/test_path/log_table/")