from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql.functions import from_json, col, expr, window, avg, exp, current_timestamp, to_timestamp, split
from pyspark.sql import functions as F


# Initialize Spark Session
spark = SparkSession.builder \
    .appName("Kafka Stream Display Example") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1") \
    .master("local[*]") \
    .getOrCreate()

# Kafka parameters
kafka_bootstrap_servers = "localhost:9092"
kafka_topic = "wikipedia-data"

# Read streaming data from Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", kafka_topic) \
    .load()

# Kafka stores the value as a binary field, so cast it to string
text_df = df.selectExpr("CAST(value AS STRING)")

# Split the lines into columns using space as the delimiter
split_df = text_df.withColumn("split_values", split(col("value"), " "))

parsed_df = split_df.select(
    col("split_values").getItem(0).alias("langDomain"),
    col("split_values").getItem(1).alias("page_title"),
    col("split_values").getItem(2).alias("page_number"),
    col("split_values").getItem(3).alias("device"),
    col("split_values").getItem(4).cast(IntegerType()).alias("unique_view_count"),
    col("split_values").getItem(5).alias("other_info"),
    current_timestamp().alias("timestamp")
)

window_duration = "1 minute"
slide_duration = "10 seconds"
decay_rate = 0.9

windowed_df = parsed_df \
    .withWatermark("timestamp", "2 minutes") \
    .groupBy(window("timestamp", window_duration, slide_duration), "page_title") \
    .agg(
        F.avg("unique_view_count").alias("avg_view_count"),
        F.expr(f"exp(sum(ln({decay_rate}) * unique_view_count) - sum(ln({decay_rate})))").alias("decayed_avg")
    )

def process_batch(batch_df, batch_id):
    # Define the output path for writing the DataFrame
    output_path = "C:/Kafka/output/test_output"

    # Write the batch DataFrame to a file in Parquet format
    batch_df.write.mode("append").parquet(output_path)

    # Optionally, you can print the batch_id or any other information for debugging
    print(f"Batch {batch_id} written to {output_path}")


# Start the streaming query with foreachBatch
query = windowed_df \
    .writeStream \
    .foreachBatch(process_batch) \
    .outputMode("update") \
    .start()

try:
    query.awaitTermination()
except KeyboardInterrupt:
    query.stop()