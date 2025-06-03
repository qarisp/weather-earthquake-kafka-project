from kafka import KafkaConsumer
from dotenv import load_dotenv
import os
import json

load_dotenv()

BOOTSTRAP_SERVER = os.getenv("BOOTSTRAP_SERVER")

consumer = KafkaConsumer(
    'bmkg_earthquakes',
    bootstrap_servers=[BOOTSTRAP_SERVER],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='console-group'
)

print("🟢 Waiting for earthquake alerts...")
for message in consumer:
    gempa = message.value
    print(f"\n🔔 GEMPA TERKINI!\nLokasi: {gempa['Wilayah']}\nMagnitude: {gempa['Magnitude']}\nPotensi: {gempa['Potensi']}")