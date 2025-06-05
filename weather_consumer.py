import json
import boto3
import os
from kafka import KafkaConsumer
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
KAFKA_TOPIC = "weather_data"
BOOTSTRAP_SERVER = os.getenv("BOOTSTRAP_SERVER")

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=[BOOTSTRAP_SERVER],
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

# Set Up DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('weather_data')

# Start consuming messages
for message in consumer:
    data = message.value
    print("Received:", data)

    try:
        item = {
            'Province': data['Province'],
            'Datetime': data['Datetime'],
            'CapitalCity': data['Capital City'],
            'TemperatureC': str(data['Temperature (C)']),
            'Weather': data['Weather'],
            'Humidity': str(data['Humidity']),
            'Pressure': str(data['Pressure (Pa)']),
            'Windspeed': str(data['Wind Speed (m/s)']),
            'lat': str(data['lat']),
            'lon': str(data['lon'])
        }

        table.put_item(Item=item)
        print(f"✅ Inserted {data['Province']} at {data['Datetime']} to DynamoDB")
    
    except Exception as e:
        print("❌ Error inserting into DynamoDB:", e)