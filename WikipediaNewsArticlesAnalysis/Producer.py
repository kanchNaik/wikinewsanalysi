import gzip
from kafka import KafkaProducer
import time
from datetime import datetime

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'  # Adjust to your Kafka server
KAFKA_TOPIC = 'wiki-pageviews_new'

# Producer configuration
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
    date, hour = extract_date_hour(filepath)
    if date is None or hour is None:
        return
    count = 0
    with gzip.open(filepath, 'rt', encoding='utf-8') as f:
        for line in f:
            count += 1
            print(count)
            # Add date and hour to each line
            enriched_line = f"{date} {hour} {line.strip()}"
            # Send message to Kafka
            producer.send(KAFKA_TOPIC, value=enriched_line)
            time.sleep(0.01)  # Adjust to control publishing rate

    producer.flush()  # Ensure all messages are delivered

publish_wiki_pageviews(r"C:\Users\naikn\Downloads\pageviews-20240131-230000.gz")
