<h1 align="center">🌦️ Indonesia Weather & Earthquake Map</h1>
<p align="center">
  A Streamlit-based interactive map visualizing real-time weather and earthquake data across Indonesia,<br/>
  powered by <strong>Apache Kafka</strong> and AWS DynamoDB.
</p>

<hr/>

<h2>📌 Features</h2>
<ul>
  <li>Displays <strong>real-time weather</strong> data (temperature, humidity, wind, weather condition) by province</li>
  <li>Visualizes <strong>earthquake alerts</strong> from across Indonesia with magnitude, depth, and location</li>
  <li>Color-coded provinces by temperature (cool → warm → hot)</li>
  <li>Hover tooltips showing detailed info per province and earthquake location</li>
  <li>Manual data refresh via sidebar</li>
</ul>

<h2>🗺️ Live Map Example</h2>
<p align="center">
  <img src="./screenshot.png" alt="Indonesia Weather Map Screenshot" width="100%" />
</p>

<h2>⚙️ Technologies Used</h2>
<ul>
  <li><strong>Python</strong> with <code>Streamlit</code> for frontend UI</li>
  <li><strong>Pydeck</strong> (Deck.gl) for interactive mapping</li>
  <li><strong>AWS DynamoDB</strong> to store weather and earthquake data</li>
  <li><strong>Apache Kafka</strong> for real-time weather data streaming and ingestion</li>
  <li><strong>Pandas</strong> and <strong>NumPy</strong> for data wrangling</li>
  <li><strong>GeoJSON</strong> for province boundary mapping</li>
</ul>

<h2>🚀 Project Architecture</h2>
<p align="center">
  <img src="./A_diagram_illustrates_the_architecture_of_an_Indon.png" alt="Architecture Diagram" width="90%" />
</p>
<p align="center"><em>Includes Kafka producer-consumer pipeline for weather data streaming</em></p>

<h2>📁 Folder Structure</h2>

<pre>
📦 indonesia-weather-map/
├── 📄 app.py               # Main Streamlit app
├── 📄 kafka_producer.py    # Kafka producer to stream weather data
├── 📄 kafka_consumer.py    # Kafka consumer to ingest and store data in DynamoDB
├── 📄 README.md            # Project documentation
├── 📄 requirements.txt     # Python dependencies
├── 📄 indonesia-province-simple.json  # GeoJSON boundaries
└── 📸 screenshot.png       # App screenshot
</pre>

<h2>🔧 Setup Instructions</h2>

<ol>
  <li>Clone the repository:
    <pre><code>git clone https://github.com/yourusername/indonesia-weather-map</code></pre>
  </li>
  <li>Install dependencies:
    <pre><code>pip install -r requirements.txt</code></pre>
  </li>
  <li>Start Apache Kafka server locally or use a cloud Kafka provider (e.g., Confluent Cloud).</li>
  <li>Run the Kafka producer to stream weather data:
    <pre><code>python kafka_producer.py</code></pre>
  </li>
  <li>Run the Kafka consumer to push data to DynamoDB:
    <pre><code>python kafka_consumer.py</code></pre>
  </li>
  <li>Configure AWS credentials (required for accessing DynamoDB):<br/>
    Ensure your environment has the necessary <code>AWS_ACCESS_KEY_ID</code> and <code>AWS_SECRET_ACCESS_KEY</code> variables or set up with AWS CLI.
  </li>
  <li>Run the Streamlit app:
    <pre><code>streamlit run app.py</code></pre>
  </li>
</ol>

<h2>📝 Todo</h2>
<ul>
  <li>[ ] Add live weather API integration (e.g., OpenWeatherMap)</li>
  <li>[ ] Improve mobile responsiveness</li>
  <li>[ ] Add unit tests and CI/CD pipeline</li>
</ul>

<h2>📬 Contact</h2>
<p>Feel free to reach out or contribute! Open an issue or fork the repo.</p>
<p><strong>Author:</strong> <a href="https://github.com/yourusername">@yourusername</a></p>
