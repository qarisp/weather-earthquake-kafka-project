import requests
from dotenv import load_dotenv
import os
import logging
from time import sleep

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

# BMKG url
URL = os.getenv("BMKG_URL")

last_event_id = None

def fetch_latest_earthquake():
    URL = os.getenv("BMKG_URL")

    try:
        response = requests.get(URL)
        if response.status_code == 200:
            gempa = response.json().get('Infogempa', {}).get('gempa', {})
            event_id = gempa.get('Tanggal') + gempa.get('Jam')

            return event_id, gempa
    except Exception as e:
        logging.error("Error getting data: {e}")
    return None

while True:
    event_id, gempa = fetch_latest_earthquake()
    if event_id and event_id != last_event_id:
        last_event_id = event_id
        logging.info(f"New earthquake event: {event_id}")
    sleep(30)