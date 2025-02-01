from pyspark.sql import SparkSession

# Create a SparkSession
spark = SparkSession.builder \
    .appName("Read Parquet Parts") \
    .getOrCreate()

# Path to the directory containing the parts
parquet_dir = r"C:\Kafka\output\slidingwindow_output"

# Read all parts into a DataFrame
df = spark.read.parquet(parquet_dir)

# Show data
df.show()
