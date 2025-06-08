<h1 align="center">🌦️ Indonesia Weather & Earthquake Map</h1>
<p align="center">
  A Streamlit-based interactive map visualizing weather and earthquake data across Indonesia,<br/>
  powered by <strong>Apache Kafka</strong> and <strong>AWS DynamoDB</strong>.
</p>

<hr/>

<h2>📌 Features</h2>
<ul>
  <li>Displays <strong>weather data</strong> (temperature, humidity, wind, weather condition) by province</li>
  <li>Visualizes <strong>earthquake location</strong> from across Indonesia with magnitude, depth, and location</li>
  <li>Color-coded provinces by temperature (cool → warm → hot)</li>
  <li>Hover tooltips showing detailed info per province</li>
  <li>Manual data refresh via sidebar</li>
</ul>

<h2>🗺️ Map Example</h2>
<p align="center">
  <img src="assets/img/map-example.png" alt="Indonesia Weather Map Screenshot" width="100%" />
</p>

<h2>⚙️ Technologies Used</h2>
<ul>
  <li><strong>Apache Kafka</strong> for weather & earthquake data streaming and ingestion</li>
  <li><strong>AWS DynamoDB</strong> to store weather and earthquake data</li>
  <li><strong>Python</strong> with <code>Streamlit</code> for frontend UI</li>
  <li><strong>Pydeck</strong> (Deck.gl) for interactive mapping</li>
  <li><strong>Pandas</strong> and <strong>NumPy</strong> for data wrangling</li>
  <li><strong>GeoJSON</strong> for province boundary mapping</li>
</ul>

<h2>🚀 Project Architecture</h2>
<p align="center">
  <img src="assets/img/architecture-diagram.jpg" alt="Architecture Diagram" width="90%" />
</p>

<p><strong>Author:</strong> <a href="https://github.com/qarisp">@qarisp</a></p>
