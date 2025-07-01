import machine
import dht
import time
import influxSender
import wifiConnection


wifi_ip = wifiConnection.connect()
print("Pico IP:", wifi_ip)


# --- ADC setup for light sensors ---
adc_sun = machine.ADC(0)   # GP26
adc_shade = machine.ADC(1) # GP27
adc_mcp = machine.ADC(2)   # GP28 = MCP9700 analog temp
led_green = machine.Pin(10, machine.Pin.OUT)
led_yellow = machine.Pin(9, machine.Pin.OUT)
led_red = machine.Pin(8, machine.Pin.OUT)

# --- DHT11 Setup ---
dht11_pin = machine.Pin(17)
dht11 = dht.DHT11(dht11_pin)

# --- Hall Effect Sensor Setup ---
hall_pin = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)
led_bench_green = machine.Pin(6, machine.Pin.OUT)
led_bench_red = machine.Pin(7, machine.Pin.OUT)

# --- Review buttons (1 to 5 stars) ---
button_pins = [11, 12, 13, 14, 15]
buttons = [machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP) for pin in button_pins]

total_reviews = 0
total_score = 0
avg_score = 0

VREF = 3.3        # ADC reference voltage
ADC_RES = 65535   # 16-bit ADC
MCP9700_V0 = 0.5   # 500mV at 0°C
MCP9700_TCOEFF = 0.01  # 10mV per °C

# Store previous temperature for rain detection
last_dht_temp = None

# Convert ADC to voltage
def read_voltage(adc):
    return adc.read_u16() * VREF / ADC_RES

# Convert analog voltage to temperature
def read_mcp9700_temp():
    voltage = read_voltage(adc_mcp)
    return round((voltage - MCP9700_V0) / MCP9700_TCOEFF, 1)

# Calculate "Feels-like" with Rothfusz regression
def compute_heat_index(temp_c, humidity):
    # Convert to Fahrenheit
    T = temp_c * 9 / 5 + 32
    R = humidity

    # Heat index formula
    HI = -42.379 + 2.04901523*T + 10.14333127*R \
         - 0.22475541*T*R - 0.00683783*T*T \
         - 0.05481717*R*R + 0.00122874*T*T*R \
         + 0.00085282*T*R*R - 0.00000199*T*T*R*R

    # Convert back to Celsius
    return round((HI - 32) * 5 / 9, 1)


while True:
    try:
        # --- Read light sensor voltages ---
        sun_voltage = read_voltage(adc_sun)
        shade_voltage = read_voltage(adc_shade)
        sun_score = round(sun_voltage - shade_voltage, 2)

        # --- Read DHT11 ---
        dht11.measure()
        dht_temp = dht11.temperature()
        dht_hum = dht11.humidity()

        # --- Rain Chance Estimation ---
        rain_chance = "Low"
        if dht_hum > 90:
            if last_dht_temp is not None and dht_temp < last_dht_temp:
                rain_chance = "High"
            elif last_dht_temp is None:
                rain_chance = "Unknown"
        last_dht_temp = dht_temp

        # MCP9700 reading (in sun)
        mcp_temp = read_mcp9700_temp()

        # Feels-like approximation
        feels_like = compute_heat_index(dht_temp, dht_hum)

        # --- Read Hall sensor (sitting detection) ---
        sitting = hall_pin.value() == 0

        # --- LEDs for bench status ---
        if sitting:
            led_bench_green.value(0)
            led_bench_red.value(1)
        else:
            led_bench_green.value(1)
            led_bench_red.value(0)

        # --- 5 button review system ---
        for idx, button in enumerate(buttons):
            if button.value() == 0:
                stars = idx + 1
                total_reviews += 1
                total_score += stars
                avg_score = round(total_score / total_reviews, 2)
                print(f"Pressed {stars} stars. Average: {avg_score} from {total_reviews} reviews.")
                time.sleep(0.3)  # debounce
        
        # --- Read light sensor voltages ---
        sun_voltage = read_voltage(adc_sun)
        shade_voltage = read_voltage(adc_shade)
        sun_score = round(sun_voltage - shade_voltage, 2)

        # --- Determine which LED to light ---
        if sun_score < 0.2:
            led_green.value(1)
            led_yellow.value(0)
            led_red.value(0)
        elif sun_score < 0.6:
            led_green.value(0)
            led_yellow.value(1)
            led_red.value(0)
        else:
            led_green.value(0)
            led_yellow.value(0)
            led_red.value(1)
        
        # --- Display output ---
        print("------------------------------")
        print(f"DHT11 Temp: {dht_temp} C")
        print(f"Humidity: {dht_hum} %")
        print(f"Feels Like: {feels_like} C")
        print(f"Rain Chance: {rain_chance}")

        if sun_score < 0.2:
            print("Mostly shaded")
        elif sun_score < 0.6:
            print("Partial sun")
        else:
            print("Full sun exposure")

        print("Someone is sitting on the bench" if sitting else "Bench is empty")
        if total_reviews > 0:
            avg_score = round(total_score / total_reviews, 2)
            print(f"Current average comfort rating: {avg_score} stars from {total_reviews} reviews")
        else:
            print("No reviews yet.")
        print("------------------------------")

    except Exception as e:
        print("Error:", e)

    influxSender.send_sensor_data(dht_temp, dht_hum, feels_like, rain_chance, sun_score, sitting, avg_score, total_reviews)

    time.sleep(2)

