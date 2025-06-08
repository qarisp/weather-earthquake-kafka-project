import streamlit as st
import pandas as pd
import pydeck as pdk
import json
import numpy as np
import boto3
from datetime import datetime

st.set_page_config(
    page_title="Indonesia Weather & Earthquake Map",
    layout="wide",  # This makes the page full-width
    initial_sidebar_state="auto"
)

st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        min-width: 300px;
        width: fit-content;
        max-width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Ensure session state is initialized
if "refresh" not in st.session_state:
    st.session_state.refresh = False

# Add the button and only trigger rerun when clicked
if st.sidebar.button("🔄 Refresh Weather & Earthquake Data"):
    st.session_state.refresh = True

# Trigger rerun only once after button click
if st.session_state.refresh:
    st.session_state.refresh = False
    st.rerun()

# Sidebar
st.sidebar.markdown("Weather last refreshed:")
st.sidebar.markdown(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.sidebar.markdown("")

# Load weather data
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')
weather_table = dynamodb.Table('weather_data')
weather_response = weather_table.scan()
weather_items = weather_response['Items']

weather_df = pd.DataFrame(weather_items)

# Load earthquake data
earthquake_table = dynamodb.Table('EarthquakeAlerts')
earthquake_response = earthquake_table.scan()
earthquake_items = earthquake_response['Items']

earthquake_df = pd.DataFrame(earthquake_items)

st.sidebar.markdown("🔔 GEMPA TERKINI")
latest_eq = earthquake_df.iloc[0]
st.sidebar.markdown(f"""
**Tanggal:** {latest_eq['tanggal']}\n
**Jam:** {latest_eq['jam']}\n
**Lokasi Gempa:** {latest_eq['wilayah']}\n
**Magnitude:** {latest_eq['magnitude']}\n
**Kedalaman:** {latest_eq['kedalaman']}\n
""")

# Parse earthquake coordinates
def parse_coords(coord_str):
    try:
        lat, lon = map(float, coord_str.split(","))
        return lat, lon
    except:
        return None, None

earthquake_df["latitude"], earthquake_df["longitude"] = zip(*earthquake_df["koordinat"].apply(parse_coords))
earthquake_df["magnitude"] = earthquake_df["magnitude"].astype(float)
earthquake_df["radius"] = earthquake_df["magnitude"] * 10000  # Adjust scale as needed
earthquake_df = earthquake_df.dropna(subset=["latitude", "longitude"])

# Load GeoJSON province boundaries
with open("indonesia-province-simple.json", "r", encoding="utf-8") as f:
    provinces_geojson = json.load(f)

# Normalize temperature to RGB
def temperature_to_color(temp):
    if temp is None:
        return [200, 200, 200, 80]  # Gray for unknown
    t = np.clip((temp - 20) / (35 - 20), 0, 1)
    r = int(255 * t)
    g = int(255 * (1 - t))
    return [r, g, 0, 160]

# Create mapping from province to color
province_colors = {}
for _, row in weather_df.iterrows():
    province_name = row["province"].upper()
    temp = row["temperature"]
    province_colors[province_name] = temperature_to_color(temp)

# Apply color and weather info to each GeoJSON feature
for feature in provinces_geojson["features"]:
    province_name = feature["properties"]["Propinsi"].upper()
    color = province_colors.get(province_name, [200, 200, 200, 80])
    feature["properties"]["color"] = color

    # Add weather data to properties (cast to JSON-safe types)
    match = weather_df[weather_df["province"].str.upper() == province_name]
    if not match.empty:
        row = match.iloc[0]
        feature["properties"]["Temperature"] = float(row["temperature"])
        feature["properties"]["Weather"] = str(row["weather"])
        feature["properties"]["Humidity"] = int(row["humidity"])
        feature["properties"]["Wind"] = float(row["wind_speed"])

# Weather GeoJson layer
weather_layer = pdk.Layer(
    "GeoJsonLayer",
    provinces_geojson,
    get_fill_color="properties.color",
    pickable=True,
    auto_highlight=True
)

# Earthquake scatterplot layer
earthquake_layer = pdk.Layer(
    "ScatterplotLayer",
    data=earthquake_df,
    get_position='[longitude, latitude]',
    get_radius='radius',
    get_fill_color='[255, 0, 0, 160]',
    pickable=False
)

# Define the view state
view_state = pdk.ViewState(
    latitude=-2.5,
    longitude=118,
    zoom=4
)

# Streamlit UI
st.title("Indonesia Weather & Earthquake Map")

# Show color legend
st.markdown("""
<div style="padding: 10px 0;">
    <strong>Legend:</strong>
    <div style="display: flex; gap: 15px; align-items: center; margin-top: 5px; flex-wrap: wrap;">
        <div style="display: flex; align-items: center; gap: 5px;">
            <div style="width: 30px; height: 15px; background-color: rgb(0, 255, 0);"></div><span>Cool</span>
        </div>
        <div style="display: flex; align-items: center; gap: 5px;">
            <div style="width: 30px; height: 15px; background-color: rgb(255, 165, 0);"></div><span>Warm</span>
        </div>
        <div style="display: flex; align-items: center; gap: 5px;">
            <div style="width: 30px; height: 15px; background-color: rgb(255, 0, 0);"></div><span>Hot</span>
        </div>
        <div style="display: flex; align-items: center; gap: 5px;">
            <div style="width: 15px; height: 15px; background-color: red; border-radius: 50%;"></div><span>Earthquake</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.pydeck_chart(pdk.Deck(
    layers=[weather_layer, earthquake_layer],
    initial_view_state=view_state,
    tooltip={
        "html": """
        <b>{Propinsi}</b><br/>
        Temp: {Temperature} °C<br/>
        Weather: {Weather}<br/>
        Humidity: {Humidity}%<br/>
        Wind: {Wind} m/s
        """,
        "style": {"backgroundColor": "steelblue", "color": "white"}
    }
))
