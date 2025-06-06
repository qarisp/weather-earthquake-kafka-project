import json
import boto3
import os
from kafka import KafkaConsumer
from dotenv import load_dotenv
from decimal import Decimal

load_dotenv()
KAFKA_TOPIC = "weather_data"
BOOTSTRAP_SERVER = os.getenv("BOOTSTRAP_SERVER")

# Set Up DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('weather_data')

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=[BOOTSTRAP_SERVER],
    group_id='weather-consumer',
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    auto_offset_reset='latest',
    enable_auto_commit=True
)

def insert_weather_data(weather):
    item = {
        'datetime': weather['Datetime'],
        'province': weather['Province'],
        'capital_city': weather['Capital City'],
        'temperature': Decimal(str(weather['Temperature (C)'])),
        'weather': weather['Weather'],
        'humidity': str(weather['Humidity (%)']),
        'pressure': str(weather['Pressure (Pa)']),
        'wind_speed': Decimal(str(weather['Wind Speed (m/s)'])),
        'lat': Decimal(str(weather['lat'])),
        'lon': Decimal(str(weather['lon']))
    }

    try:
        table.put_item(Item=item)
        print("✅ Inserted into DynamoDB:", item['province'])
    except Exception as e:
        print("❌ Error inserting to DynamoDB:", e)

print("🟢 Weather DynamoDB Consumer Started...")
for message in consumer:
    weather = message.value
    insert_weather_data(weather)