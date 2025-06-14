from kafka import KafkaConsumer
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
BOOTSTRAP_SERVER = os.getenv("BOOTSTRAP_SERVER")

consumer = KafkaConsumer(
    'bmkg_earthquakes',
    bootstrap_servers=[BOOTSTRAP_SERVER],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='telegram-group'
)

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': text}
    requests.post(url, json=payload)

print("📨 Listening for Telegram alert messages...")
for message in consumer:
    gempa = message.value
    msg = (
        f"🔔 GEMPA TERKINI\n"
        f"Wilayah: {gempa['Wilayah']}\n"
        f"Magnitude: {gempa['Magnitude']}\n"
        f"Potensi: {gempa['Potensi']}\n"
        f"Waktu: {gempa['Tanggal']} {gempa['Jam']}\n\n"
        f"📡 Data by BMKG ©"
    )
    send_telegram_message(msg)