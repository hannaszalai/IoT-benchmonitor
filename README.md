<div align="center">
<img src="assets/images/readme-title.png" alt="Lake Balaton Bench Logger" width="250">
</div>

## Table of Content
[Author](#author)  
[Project Overview](#project-overview)  
[Estimated Time](#estimated-time)
[Project Objective](#project-objective)  
[Bill of Material](#bill-of-material)  
[Raspberry Pi Pico W setup](#raspberry-pi-pico-w-setup)  
[Wiring](#wiring)  
[Environmental Comfort Calculation](#environmental-comfort-calculation)  
[Transmitting Data](#transmitting-data)  
[Data Storage and Visualization](#data-storage-and-visualization)  
[The Code](#the-code)  
[Development Phases](#development-phases)  
[Useful Links](#useful-links)

![Lake Balaton Bench](assets/images/header.png)

## Author
Made by Hanna Szalai (hs223xt)

## Project Overview  
Each summer, thousands of people circle Lake Balaton by bike or foot, seeking the **perfect bench to relax on**. But what makes a bench perfect? Is it the view, the temperature, the breeze, or the warm sunshine on your shoulders?  
This small IoT project tries to figure that out.  
A device was placed under one of Balaton’s most iconic benches to monitor:
- when people sit down,
- how warm and humid it is,
- how bright the sun is,
- plus it lets people vote with a 1–5 star button.
All this data flows into a colorful online dashboard, showing:
- real-time comfort scores,
- weather alerts,
- and historical trends. 
Think of it as TripAdvisor for benches.

![Map](assets/images/map.png)


## Estimated Time
| Task | Time |
|------|------|
| Hardware prototyping | 1,5 hours |
| MicroPython firmware | 2 hours |
| Docker (TIG stack) setup | 3 hours |
| Frontend + dashboard tweaks | 2 hours |
| Testing & polishing | 1,5 hours |
| **Total:** | **~10 hours** |

## Project Objective
- Create a low-power, WiFi-connected device that monitors bench comfort.
- Store & visualize the data using InfluxDB + Grafana in Docker.
- Let people give their own ratings via buttons.
- Display it all on a custom Flask web dashboard with real-time updates and Chart.js visualizations.


## Bill of Material
| Image | Component | Price (SEK) | Purpose |Add commentMore actions
|-------|-----------|-------------|---------|
| <img src="https://www.electrokit.com/cache/ba/700x700-product_41019_41019114_PICO-WH-HERO.jpg" alt="Raspberry Pi Pico W" width="100"> | Raspberry Pi Pico WH | 99 SEK | Main microcontroller with WiFi |
| ![alt text](assets/images/image.png) | Breadboard | 69 SEK | Prototyping platform |
| ![alt text](assets/images/image-1.png) | USB cable | 49 SEK | Power and programming |
| ![alt text](assets/images/image-2.png) | Lab cable M/M, F/M | 49 SEK | Connections between components |
| ![alt text](assets/images/image-3.png) | Digital temperature and humidity sensor DHT11 | 49 SEK | Environmental sensing |
| ![alt text](assets/images/image-4.png) | TLV49645 SIP-3 Hall effect sensor digital | 12,5 SEK | Magnetic field detection |
| ![alt text](assets/images/image-5.png) | MCP9700 TO-92 Temperature sensor | 11,5 SEK | Temperature monitoring |
| ![alt text](assets/images/image-6.png) | Photoresistor CdS 4-7 kohm | 9 SEK | Light level detection |
| ![alt text](assets/images/image-7.png) | LEDs | 15 SEK | Status indicators |
| ![alt text](assets/images/image-9.png) | Carbon film resistors | 25 SEK | Current limiting |
| ![alt text](assets/images/image-10.png) | Magnet Neo35 Ø5mm x 5mm | 11 SEK | Hall sensor trigger |
| ![alt text](assets/images/image-11.png) | Tactile switch PCB 6x6x5mm black | 1,25 SEK | User input button |
= total price = ... SEK

## Raspberry Pi Pico W setup
- Plug it into your computer while pressing the reboot button, then copy the .UF2 file into the pico.  
  More information here: https://micropython.org/download/RPI_PICO_W/
- Download VS Code, follow the tutorial here: https://code.visualstudio.com/download
- Then install the Python extension:

![Python Extension](assets/images/python.png)

- And install the MicroPico extension to run the pico files:

![MicroPico Extension](assets/images/micropico.png)



## Wiring
TODO: fritzing diagram


## Calculations

### ⚠ Disclaimer
This is an approximation. Do not rely solely on these calculations if you want to replicate this project.  
Always verify all connections, resistor values, and current ratings yourself to ensure safety and proper functioning.


| Component                        | Operating Voltage | Current (approx) | Resistor Needed | Remarks                           |
|-----------------------------------|-------------------|------------------|-----------------|-----------------------------------|
| Raspberry Pi Pico W               | 3.3V               | ~50 mA idle      | -               | Powers everything, connects via WiFi |
| DHT11 Temp+Humidity Sensor        | 3.3V               | ~2.5 mA          | -               | On `GP17` (Pin 22) |
| MCP9700 Analog Temp Sensor        | 3.3V               | <1 mA            | -               | On `ADC2` (GP28) |
| CdS Photoresistor (light sensor)  | 3.3V               | <1 mA            | Voltage divider | On `ADC0` (GP26) & `ADC1` (GP27) |
| Hall Effect Sensor                | 3.3V               | ~4 mA            | -               | On `GP16` (Pin 21), detects sitting |
| 3x Status LEDs (green/yellow/red) | 3.3V               | ~20 mA each      | ~220Ω each      | On `GP8`, `GP9`, `GP10` |
| 2x Bench LEDs                     | 3.3V               | ~20 mA each      | ~220Ω each      | On `GP6`, `GP7` |
| 5x Rating Buttons                 | -                  | - (pulled up)    | -               | On `GP11-15`, uses internal pull-up |
| WiFi Module (built-in)            | 3.3V               | ~50-120 mA active| -               | For MQTT/HTTP uploads |

**Total Estimated Current:**  
≈ 50 mA (Pico) + sensors + LEDs + WiFi peaks ≈ 150-180 mA max


### Environmental Comfort Calculation  
The device uses several calculations to interpret environmental readings:

#### 1. ADC to Voltage Conversion
```python
def read_voltage(adc):
    return adc.read_u16() * VREF / ADC_RES

# Constants:
VREF = 3.3        # ADC reference voltage
ADC_RES = 65535   # 16-bit ADC resolution
```

#### 2. MCP9700 Temperature Sensor Reading
```python
def read_mcp9700_temp():
    voltage = read_voltage(adc_mcp)
    return round((voltage - MCP9700_V0) / MCP9700_TCOEFF, 1)

# Constants:
MCP9700_V0 = 0.5      # 500mV at 0°C
MCP9700_TCOEFF = 0.01 # 10mV per °C
```

#### 3. Heat Index "Feels-Like" Calculation (Rothfusz Regression)
```python
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
```

#### 4. Sun/Shade Detection
```python
sun_voltage = read_voltage(adc_sun)
shade_voltage = read_voltage(adc_shade)
sun_score = round(sun_voltage - shade_voltage, 2)

# Classification:
if sun_score < 0.2:
    status = "Mostly shaded"
elif sun_score < 0.6:
    status = "Partial sun"
else:
    status = "Full sun exposure"
```

#### 5. Rain Chance Estimation
```python
rain_chance = "Low"
if dht_hum > 90:
    if last_dht_temp is not None and dht_temp < last_dht_temp:
        rain_chance = "High"
    elif last_dht_temp is None:
        rain_chance = "Unknown"
```

#### 6. User Rating Average
```python
# When button pressed (1-5 stars):
total_reviews += 1
total_score += stars
avg_score = round(total_score / total_reviews, 2)
```

## Transmitting Data
Explain how data moves through the system:

- How often data is collected (e.g., every 3 seconds)  
- Where it is stored (e.g., database, server)  
- What triggers data transmission  
- Optional automation (e.g., push notifications)


## Data Storage and Visualization  
### Storage  
- InfluxDB running in Docker (docker-compose.yml includes influxdb, telegraf, grafana).

### Visualization  
- Grafana dashboards display:
    - Current comfort
    - Past 24h trends
    - Star ratings over time
- Embedded in a simple static HTML page.

# The Code

## File Structure
```
IoT-benchmonitor/
├── README.md
├── LICENSE
├── docker-compose.yml          # Docker services (InfluxDB + Grafana)
│
├── micropython/                # Raspberry Pi Pico W code
│   ├── main.py                # Main sensor loop
│   ├── wifiConnection.py      # WiFi connection helper
│   └── influxSender.py        # Data transmission to InfluxDB
│
├── web/                       # Flask web application
│   ├── server.py              # Flask backend server
│   ├── index.html             # Main dashboard page
│   └── static/
│       ├── styles.css         # Dashboard styling
│       ├── script.js          # Frontend JavaScript + Chart.js
│       └── images/
│           ├── bench.png      # Bench image
│           └── icon.png       # Favicon
│
└── assets/                    # Documentation images
    └── images/
        ├── header.png         # README header image
        ├── map.png           # Project location map
        ├── micropico.png     # VS Code extension screenshot
        ├── python.png        # Python extension screenshot
        └── ...               # Other documentation images
```

## Development Phases  
Outline the project in phases:

1. Phase 1 – Terminal output (basic testing)  
![alt text](assets/images/terminal-print.png)
3. Phase 2 – Custom website with graphs and live data
![alt text](assets\images\frontend.png)


## 8. Useful Links  
- GitHub repo: https://github.com/hannaszalai/IoT-benchmonitor  
- Demo Youtube video: `[YouTube link]`