from pyspark.sql import SparkSession
from pyspark.sql.functions import col, unix_timestamp,to_timestamp
from datetime import datetime, timedelta
from pyspark.sql import functions as F
from pyspark.sql.window import Window
import pytz

# Path to the directory where the Parquet files are stored
output_dir = "C:/Kafka/output/test_output"

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("Trending Topics Analysis") \
    .getOrCreate()

# Function to read Parquet files from the last one hour
def read_parquet_files_from_last_hour(output_dir):
    try:
        # Get the current time and time 1 hour ago
        now = datetime.now()
        one_hour_ago = now - timedelta(hours=1)

        # Read all Parquet files in the directory
        data = spark.read.parquet(output_dir)

        # Ensure the 'window' column is in timestamp format
        data = data.withColumn("window", to_timestamp(col("window.start")))  # Adjust column name if needed

        # Filter the data to only include records from the last hour
        filtered_data = data.filter(col("window") >= one_hour_ago.strftime('%Y-%m-%d %H:%M:%S'))
        return data

    except Exception as e:
        print(f"Error reading parquet files: {e}")
        return None

# Function to get the top 10 trending topics based on the existing weights
def get_top_trending_topics(data):
    try:
        # Sort by the 'decayed_avg' (or 'total_weight') in descending order and get the top 10 topics
        window_spec = Window.partitionBy("page_title").orderBy(F.col("window").desc())

        # Step 2: Add a column to identify the most recent record in each group
        data_with_rank = data.withColumn("rank", F.row_number().over(window_spec))

        # Step 3: Filter to keep only the most recent record per page_title
        most_recent = data_with_rank.filter(F.col("rank") == 1)

        # Step 4: Aggregate to sum the pageviews and keep the most recent decayed_avg
        top_topics = (
            most_recent.groupBy("page_title")
            .agg(
                F.sum("avg_view_count").alias("total_pageviews"),  # Sum pageviews
                F.first("decayed_avg").alias("decayed_avg")  # Most recent decayed_avg
            )
            .filter(F.col("total_pageviews") > 1) 
            .orderBy(F.col("decayed_avg").desc())  # Sort by decayed_avg
            .limit(100)  # Keep the top 10 results
        )

        return top_topics
    except Exception as e:
        print(f"Error processing trending topics: {e}")
        return None