import urequests
import time

# InfluxDB configuration
INFLUXDB_URL = "http://192.168.0.61:8086/api/v2/write?org=my-org&bucket=my-bucket&precision=s"
INFLUXDB_TOKEN = "my-token"

HEADERS = {
    "Authorization": f"Token {INFLUXDB_TOKEN}",
    "Content-Type": "text/plain"
}

def send_sensor_data(dht_temp, dht_hum, feels_like, rain_chance, sun_score, sitting, avg_score, total_reviews):
    """
    Send sensor data to InfluxDB using line protocol format.
    Returns True if successful, False otherwise.
    """
    try:
        # Map rain_chance string to numeric value for easier querying
        rain_value = 1 if rain_chance == "High" else 0
        
        # Convert boolean sitting to integer
        sitting_value = 1 if sitting else 0
        
        # Build InfluxDB line protocol payload
        # Format: measurement field1=value1,field2=value2 timestamp
        payload = (
            f"bench_data "
            f"temperature={dht_temp},"
            f"humidity={dht_hum},"
            f"feels_like={feels_like},"
            f"rain_chance={rain_value},"
            f"sun_score={sun_score},"
            f"sitting={sitting_value},"
            f"avg_rating={avg_score},"
            f"total_reviews={total_reviews}"
        )
                
        response = urequests.post(INFLUXDB_URL, headers=HEADERS, data=payload)
        
        if response.status_code == 204:
            print("Data sent successfully to InfluxDB")
            response.close()
            return True
        else:
            print(f"InfluxDB error: {response.status_code} - {response.text}")
            response.close()
            return False
            
    except Exception as e:
        print(f"Failed to send to InfluxDB: {e}")
        return False
