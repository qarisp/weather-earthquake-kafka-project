import streamlit as st
import pandas as pd
import pydeck as pdk
import json
import numpy as np
import boto3
from datetime import datetime

st.set_page_config(
    page_title="Indonesia Weather Map",
    layout="wide",  # This makes the page full-width
    initial_sidebar_state="auto"
)

# Ensure session state is initialized
if "refresh" not in st.session_state:
    st.session_state.refresh = False

# Add the button and only trigger rerun when clicked
if st.sidebar.button("🔄 Refresh Weather Data"):
    st.session_state.refresh = True

# Trigger rerun only once after button click
if st.session_state.refresh:
    st.session_state.refresh = False
    st.rerun()

# ✅ Optional: show last refreshed time
st.sidebar.markdown(f"Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Load weather data
dymanodb = boto3.resource('dynamodb')
table = dymanodb.Table('weather_data')

response = table.scan()
items = response['Items']

df = pd.DataFrame(items)

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
for _, row in df.iterrows():
    province_name = row["province"].upper()
    temp = row["temperature"]
    province_colors[province_name] = temperature_to_color(temp)

# Apply color and weather info to each GeoJSON feature
for feature in provinces_geojson["features"]:
    province_name = feature["properties"]["Propinsi"].upper()
    color = province_colors.get(province_name, [200, 200, 200, 80])
    feature["properties"]["color"] = color

    # Add weather data to properties (cast to JSON-safe types)
    match = df[df["province"].str.upper() == province_name]
    if not match.empty:
        row = match.iloc[0]
        feature["properties"]["Temperature"] = float(row["temperature"])
        feature["properties"]["Weather"] = str(row["weather"])
        feature["properties"]["Humidity"] = int(row["humidity"])
        feature["properties"]["Wind"] = float(row["wind_speed"])

# Define the pydeck GeoJsonLayer
layer = pdk.Layer(
    "GeoJsonLayer",
    provinces_geojson,
    get_fill_color="properties.color",
    pickable=True,
    auto_highlight=True
)

# Define the view state
view_state = pdk.ViewState(
    latitude=-2.5,
    longitude=118,
    zoom=4
)

# Streamlit UI
st.title("🌡️ Indonesia Weather Map by Province")

# Show color legend
st.markdown("""
<div style="padding: 10px 0;">
    <strong>Temperature Color Legend:</strong>
    <div style="display: flex; gap: 10px; align-items: center; margin-top: 5px;">
        <div style="width: 30px; height: 15px; background-color: rgb(0, 255, 0);"></div><span>Cool</span>
        <div style="width: 30px; height: 15px; background-color: rgb(255, 165, 0);"></div><span>Warm</span>
        <div style="width: 30px; height: 15px; background-color: rgb(255, 0, 0);"></div><span>Hot</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.pydeck_chart(pdk.Deck(
    layers=[layer],
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
