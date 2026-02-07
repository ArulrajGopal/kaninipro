#!/bin/bash


# Check if a script file is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <pyspark_script.py>"
    exit 1
fi

PYSPARK_SCRIPT="$1"

# Directory to store Spark event logs
EVENT_LOG_DIR="/home/Arulraj/Desktop/spark_events/"

# Make sure the directory exists
mkdir -p "$EVENT_LOG_DIR"

# Check if Spark History Server is running
if pgrep -f "org.apache.spark.deploy.history.HistoryServer" > /dev/null; then
    echo "Spark History Server is already running."
else
    echo "Starting Spark History Server..."
    SPARK_HISTORY_OPTS="-Dspark.history.fs.logDirectory=$EVENT_LOG_DIR" \
    "$SPARK_HOME/sbin/start-history-server.sh"
fi


spark-submit \
    --packages io.delta:delta-spark_2.13:4.0.0,org.apache.hadoop:hadoop-azure:3.3.4,com.microsoft.azure:azure-storage:8.6.6 \
    --conf spark.eventLog.enabled=true \
    --conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension \
    --conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog \
    --conf spark.eventLog.dir="file://$EVENT_LOG_DIR" \
    --num-executors 8 \
    --executor-cores 8 \
    --executor-memory 24g \
    --conf spark.executor.memoryOverhead=8g \
    --driver-memory 32g \
    --conf spark.sql.shuffle.partitions=64 \
    --conf spark.default.parallelism=64 \
    "$PYSPARK_SCRIPT"
