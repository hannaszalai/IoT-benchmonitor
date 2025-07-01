import urequests # MicroPython HTTP library for sending POST requests

# InfluxDB configuration
INFLUXDB_URL = "http://192.168.0.65:8086/api/v2/write?org=my-org&bucket=my-bucket&precision=s"
INFLUXDB_TOKEN = "my-token"

HEADERS = {
    "Authorization": f"Token {INFLUXDB_TOKEN}",
    "Content-Type": "text/plain"
}

def send_sensor_data(dht_temp, dht_hum, feels_like, rain_chance, sun_score, sitting, avg_score, total_reviews):
    # Map rain_chance string to numeric value
    rain_value = 1 if rain_chance == "High" else 0

    # Influx line protocol: measurement field=value
    payload = (
        f"bench_data "
        f"dht_temp={dht_temp},"
        f"dht_hum={dht_hum},"
        f"feels_like={feels_like},"
        f"rain={rain_value},"
        f"sun_score={sun_score},"
        f"sitting={int(sitting)},"
        f"avg_score={avg_score},"
        f"total_reviews={total_reviews}"
    )
    try:
        response = urequests.post(INFLUXDB_URL, headers=HEADERS, data=payload)
        print("InfluxDB:", response.status_code, response.text)
        response.close()
    except Exception as e:
        print("Failed to send to InfluxDB:", e)
