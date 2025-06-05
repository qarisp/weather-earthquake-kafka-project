import os
import json
import time
from kafka import KafkaProducer
from dotenv import load_dotenv
from weather_extract_transform_load import extract, transform

load_dotenv()

WEATHER_API = os.getenv("WEATHER_API_KEY")
KAFKA_TOPIC = "weather_data"
BOOTSTRAP_SERVER = os.getenv("BOOTSTRAP_SERVER")

PROVINCES = [
    {"name": "Aceh", "capital_city": "Banda Aceh", "lat": 5.5483, "lon": 95.3238},
    {"name": "Sumatra Utara", "capital_city": "Medan", "lat": 3.5952, "lon": 98.6722},
    {"name": "Sumatra Barat", "capital_city": "Padang", "lat": -0.9471, "lon": 100.4172},
    {"name": "Riau", "capital_city": "Pekanbaru", "lat": 0.5071, "lon": 101.4478},
    {"name": "Kepulauan Riau", "capital_city": "Tanjung Pinang", "lat": 0.9167, "lon": 104.4500},
    {"name": "Jambi", "capital_city": "Jambi", "lat": -1.6099, "lon": 103.6073},
    {"name": "Sumatra Selatan", "capital_city": "Palembang", "lat": -2.9909, "lon": 104.7566},
    {"name": "Bangka Belitung", "capital_city": "Pangkal Pinang", "lat": -2.1333, "lon": 106.1167},
    {"name": "Bengkulu", "capital_city": "Bengkulu", "lat": -3.8000, "lon": 102.2667},
    {"name": "Lampung", "capital_city": "Bandar Lampung", "lat": -5.4500, "lon": 105.2667},
    {"name": "Banten", "capital_city": "Serang", "lat": -6.1200, "lon": 106.1503},
    {"name": "DKI Jakarta", "capital_city": "Jakarta", "lat": -6.2088, "lon": 106.8456},
    {"name": "Jawa Barat", "capital_city": "Bandung", "lat": -6.9147, "lon": 107.6098},
    {"name": "Jawa Tengah", "capital_city": "Semarang", "lat": -6.9667, "lon": 110.4167},
    {"name": "DIY Yogyakarta", "capital_city": "Yogyakarta", "lat": -7.7956, "lon": 110.3695},
    {"name": "Jawa Timur", "capital_city": "Surabaya", "lat": -7.2504, "lon": 112.7688},
    {"name": "Bali", "capital_city": "Denpasar", "lat": -8.6705, "lon": 115.2126},
    {"name": "Nusa Tenggara Barat", "capital_city": "Mataram", "lat": -8.5833, "lon": 116.1167},
    {"name": "Nusa Tenggara Timur", "capital_city": "Kupang", "lat": -10.1772, "lon": 123.6070},
    {"name": "Kalimantan Barat", "capital_city": "Pontianak", "lat": -0.0263, "lon": 109.3425},
    {"name": "Kalimantan Tengah", "capital_city": "Palangka Raya", "lat": -2.2096, "lon": 113.9108},
    {"name": "Kalimantan Selatan", "capital_city": "Banjarbaru", "lat": -3.4420, "lon": 114.8450},
    {"name": "Kalimantan Timur", "capital_city": "Samarinda", "lat": -0.5022, "lon": 117.1537},
    {"name": "Kalimantan Utara", "capital_city": "Tanjung Selor", "lat": 2.8389, "lon": 117.3755},
    {"name": "Sulawesi Utara", "capital_city": "Manado", "lat": 1.4748, "lon": 124.8421},
    {"name": "Sulawesi Tengah", "capital_city": "Palu", "lat": -0.8917, "lon": 119.8707},
    {"name": "Sulawesi Selatan", "capital_city": "Makassar", "lat": -5.1477, "lon": 119.4327},
    {"name": "Sulawesi Tenggara", "capital_city": "Kendari", "lat": -3.9722, "lon": 122.5149},
    {"name": "Gorontalo", "capital_city": "Gorontalo", "lat": 0.5436, "lon": 123.0566},
    {"name": "Sulawesi Barat", "capital_city": "Mamuju", "lat": -2.6726, "lon": 118.8870},
    {"name": "Maluku", "capital_city": "Ambon", "lat": -3.6950, "lon": 128.1820},
    {"name": "Maluku Utara", "capital_city": "Sofifi", "lat": 0.7333, "lon": 127.3667},
    {"name": "Papua", "capital_city": "Jayapura", "lat": -2.5337, "lon": 140.7181},
    {"name": "Papua Barat", "capital_city": "Manokwari", "lat": -0.8615, "lon": 134.0620},
    {"name": "Papua Tengah", "capital_city": "Nabire", "lat": -3.3633, "lon": 135.4960},
    {"name": "Papua Pegunungan", "capital_city": "Wamena", "lat": -4.0833, "lon": 138.9500},
    {"name": "Papua Selatan", "capital_city": "Merauke", "lat": -8.4667, "lon": 140.3333},
    {"name": "Papua Barat Daya", "capital_city": "Sorong", "lat": -0.8762, "lon": 131.2610},
]

producer = KafkaProducer(
    bootstrap_servers=[BOOTSTRAP_SERVER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

while True:
    raw_data = extract(WEATHER_API, PROVINCES)
    clean_data = transform(raw_data)

    for record in clean_data:
        producer.send(KAFKA_TOPIC, value=record)
        print(f"✅ Sent weather data for {record['Province']} to Kafka")
    producer.flush()

    print("🕒 Sleeping for 5 minutes...")
    time.sleep(300)  # 300 seconds = 5 minutes