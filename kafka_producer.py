import requests
import time
import json
from kafka import KafkaProducer
from dotenv import load_dotenv
import os

load_dotenv()

BOOTSTRAP_SERVER = os.getenv("BOOTSTRAP_SERVER")

producer = KafkaProducer(
    bootstrap_servers=[BOOTSTRAP_SERVER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

last_event_id = None

def fetch_latest_earthquake():
    url = os.getenv("BMKG_URL")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            gempa = response.json().get('Infogempa', {}).get('gempa', {})
            event_id = gempa.get('Tanggal') + gempa.get('Jam')
            return event_id, gempa
    except Exception as e:
        print('Error fetching data:', e)
    return None, None

while True:
    event_id, gempa = fetch_latest_earthquake()
    if event_id and event_id != last_event_id:
        print(f"New Earthquake Event: {event_id}")
        producer.send('bmkg_earthquakes', gempa)
        last_event_id = event_id
    time.sleep(30)  # Poll every 30 seconds