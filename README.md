🌏 Indonesia Weather & Earthquake Map
A real-time, interactive Streamlit application that visualizes current weather conditions and recent earthquake activity across Indonesia. The application fetches live data from AWS DynamoDB tables and displays it on a map using PyDeck (Mapbox + WebGL).

🚀 Features
✅ Real-time weather visualization for each Indonesian province

✅ Live earthquake alerts with magnitude and depth visualization

✅ Hover tooltips with detailed meteorological and seismic data

✅ Color-coded temperature map for quick climate assessment

✅ User-triggered data refresh button with last-updated timestamp

✅ Built with Streamlit, PyDeck, and AWS DynamoDB

📸 Screenshot
(Add your screenshot here)

🏗️ Architecture
The architecture of the project consists of the following components:

Frontend: Streamlit Web App

Backend:

Weather Data Source: Weather API (fetched and stored in DynamoDB)

Earthquake Data Source: BMKG Earthquake Feed (fetched and stored in DynamoDB)

Database: AWS DynamoDB

weather_data Table: Stores latest weather data for each province

EarthquakeAlerts Table: Stores recent earthquake alerts with location info

Visualization: PyDeck with Mapbox for 3D map rendering

GeoJSON: Indonesian province borders (indonesia-province-simple.json)

