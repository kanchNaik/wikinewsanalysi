import gzip
from kafka import KafkaProducer
import time
from datetime import datetime
import sys
import os

# Get the absolute path of the 'wikinews' directory (two levels up from the current file)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Add the project root directory to sys.path
sys.path.append(project_root)

# Now you can import from Setupconstants
from wikinews.Setupconstants import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC

# Create Kafka Producer instance
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: v.encode('utf-8')  # Serialize messages to UTF-8
)

# Extract date and hour from filename
def extract_date_hour(filename):
    # Example filename: pageviews-20240101-220000.gz
    try:
        date_str = filename.split('-')[1]  # '20240101'
        hour_str = filename.split('-')[2][:2]  # '22'
        date = datetime.strptime(date_str, '%Y%m%d').strftime('%Y-%m-%d')
        hour = hour_str
        return date, hour
    except (IndexError, ValueError):
        print("Filename format is incorrect. Expected format: 'pageviews-YYYYMMDD-HHmmss.gz'")
        return None, None

# Load and send file lines to Kafka
def publish_wiki_pageviews(filepath):
    print(filepath)
    date, hour = extract_date_hour(filepath)
    if date is None or hour is None:
        return
    count = 0
    with gzip.open(filepath, 'rt', encoding='utf-8') as f:
        for line in f:
            if line.startswith("en"):
                count += 1
                print(count)
                # Add date and hour to each line
                enriched_line = f"{date} {hour} {line.strip()}"
                # Send message to Kafka
                producer.send(KAFKA_TOPIC, value=enriched_line)
                time.sleep(0.01)  # Adjust to control publishing rate

    # Wait for all messages in the producer's buffer to be delivered
    producer.flush()

