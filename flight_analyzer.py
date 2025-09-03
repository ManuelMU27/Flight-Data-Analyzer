import requests
import sqlite3
import pandas as pd 
import plotly.express as px
from sklearn.ensemble import IsolationForest  

# Gets live flights over a bounding box (latitude, longitude)  
# This link works for Georgia specifically: https://opensky-network.org/api/states/all?lamin=30.0&lomin=-85.0&lamax=35.0&lomax=-80.0
# The following lines of code are used to target a specific location, using the state of Georgia, USA as an example:
# Example: Georgia bounding box
# lamin, lomin, lamax, lomax = 30.0, -85.0, 35.0, -80.0
# url = f"https://opensky-network.org/api/states/all?lamin={lamin}&lomin={lomin}&lamax={lamax}&lomax={lomax}"

url = "https://opensky-network.org/api/states/all"
response = requests.get(url)
data = response.json()

# Converts to DataFrame
columns = ["icao24", "callsign", "origin_country", "time_position", "last_contact",
           "longitude", "latitude", "baro_altitude", "on_ground", "velocity",
           "heading", "vertical_rate", "sensors", "geo_altitude", "squawk",
           "spi", "position_source"]
df = pd.DataFrame(data['states'], columns=columns)

print(df.head())

# Flight data saved locally to query it later
conn = sqlite3.connect("flight_data.db")
df.to_sql("flights", conn, if_exists="replace", index=False)

# Test query
test_df = pd.read_sql("SELECT * FROM flights LIMIT 5;", conn)
print(test_df)

# Creates an interactive flight map showing routes and speeds
fig = px.scatter_mapbox(df,
                        lat="latitude",
                        lon="longitude",
                        hover_name="callsign",
                        hover_data=["velocity", "baro_altitude"],
                        color="origin_country",
                        zoom=5,
                        height=600)
fig.update_layout(mapbox_style="open-street-map")
fig.show()

# Drops rows with missing vertical_rate
clean_df = df.dropna(subset=["vertical_rate"])
model = IsolationForest(contamination=0.05)
clean_df['anomaly'] = model.fit_predict(clean_df[["vertical_rate"]])

# Shows anomalous flights
anomalies = clean_df[clean_df['anomaly'] == -1]
print(anomalies[["callsign", "vertical_rate"]])
