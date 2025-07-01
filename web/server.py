
from flask import Flask, jsonify, send_from_directory
from influxdb_client import InfluxDBClient
import os


# ------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------

# Flask app setup - serves static files from ./static
app = Flask(__name__, static_url_path='/static', static_folder='static')

# InfluxDB client configuration
INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "my-token"
INFLUX_ORG = "my-org"
INFLUX_BUCKET = "my-bucket"

# Create InfluxDB client and query API
client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
query_api = client.query_api()


# ------------------------------------------------------
# ROUTES
# ------------------------------------------------------

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/data")
def get_data():
    # Flux query to get the last 10 minutes of bench data
    query = f'''
    from(bucket: "{INFLUX_BUCKET}")
    |> range(start: -10m)
    |> filter(fn: (r) => r._measurement == "bench_data")
    |> filter(fn: (r) => r._field == "dht_temp" or r._field == "dht_hum" or r._field == "sun_score" or 
                            r._field == "feels_like" or r._field == "rain_chance" or r._field == "sitting" or 
                            r._field == "avg_score" or r._field == "total_reviews")
    |> keep(columns: ["_time", "_field", "_value"])
    '''

    # Run the query
    tables = query_api.query(org=INFLUX_ORG, query=query)
    
    # Prepare data structures for each field
    temp, hum, sun, feels, rain, sitting = [], [], [], [], [], []
    avg_scores, total_reviews = [], []

    # Parse query results into JSON lists
    for table in tables:
        for record in table.records:
            t = record.get_time().isoformat()
            v = record.get_value()
            f = record.get_field()

            if f == "dht_temp":
                temp.append({ "time": t, "value": v })
            elif f == "dht_hum":
                hum.append({ "time": t, "value": v })
            elif f == "sun_score":
                sun.append({ "time": t, "value": v })
            elif f == "feels_like":
                feels.append({ "time": t, "value": v })
            elif f == "rain":
                rain.append({ "time": t, "value": v })
            elif f == "sitting":
                sitting.append({ "time": t, "value": v })
            elif f == "avg_score":
                avg_scores.append({ "time": t, "value": v })
            elif f == "total_reviews":
                total_reviews.append({ "time": t, "value": v })

    # Return everything as a single JSON object
    return jsonify({
        "temp": temp,
        "hum": hum,
        "sun": sun,
        "feels": feels,
        "rain": rain,
        "sitting": sitting,
        "avg_scores": avg_scores,
        "total_reviews": total_reviews,
    })


# ------------------------------------------------------
# ENTRY POINT
# ------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
