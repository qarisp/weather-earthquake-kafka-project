from kafka import KafkaConsumer
import boto3
import json
from datetime import datetime, timezone
from decimal import Decimal
from dotenv import load_dotenv
import os

load_dotenv()
BOOTSTRAP_SERVER = os.getenv("BOOTSTRAP_SERVER")

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EarthquakeAlerts')

consumer = KafkaConsumer(
    'bmkg_earthquakes',
    bootstrap_servers=[BOOTSTRAP_SERVER],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='dynamodb-consumer-group'
)

def insert_earthquake_event(gempa):
    item = {
        'id': f"{gempa['Tanggal']}T{gempa['Jam']}_{gempa['Wilayah']}",
        'wilayah': gempa['Wilayah'],
        'koordinat': gempa['Coordinates'],
        'magnitude': Decimal(str(gempa['Magnitude'])),
        'kedalaman': gempa['Kedalaman'],
        'potensi': gempa['Potensi'],
        'tanggal': gempa['Tanggal'],
        'jam': gempa['Jam'],
        'timestamp': datetime.now(timezone.utc).isoformat()
    }
    try:
        table.put_item(Item=item)
        print("✅ Inserted into DynamoDB:", item['id'])
    except Exception as e:
        print("❌ Error inserting to DynamoDB:", e)


print("🟢 Earthquake DynamoDB Consumer Started...")
for message in consumer:
    gempa = message.value
    insert_earthquake_event(gempa)