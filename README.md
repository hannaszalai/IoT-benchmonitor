# Lake Balaton Bench Logger
*“Find the best benches to relax by the lake!”*
![Lake Balaton Bench](assets/images/header.png)

---

## Table of Content
- [Author](#author)
- [Project Overview](#project-overview)
- [Estimated Time](#estimated-time)
- [Project Objective](#project-objective)
- [Bill of Material](#bill-of-material)
- [Raspberry Pi Pico W setup](#raspberry-pi-pico-w-setup)
- [Wiring](#wiring)
- [Environmental Comfort Calculation](#environmental-comfort-calculation)
- [Transmitting Data](#transmitting-data)
- [Data Storage and Visualization](#data-storage-and-visualization)
- [The Code](#the-code)
- [Development Phases](#development-phases)
- [Useful Links](#useful-links)

---

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

---

## Estimated Time
| Task | Time |
|------|------|
| Hardware prototyping | 1,5 hours |
| MicroPython firmware | 2 hours |
| Docker (TIG stack) setup | 3 hours |
| Frontend + dashboard tweaks | 2 hours |
| Testing & polishing | 1,5 hours |
| **Total:** | **~10 hours** |
---

## Project Objective
- Create a low-power, WiFi-connected device that monitors bench comfort.
- Store & visualize the data using InfluxDB + Grafana in Docker.
- Let people give their own ratings via buttons.
- Display it all on a custom Flask web dashboard with real-time updates and Chart.js visualizations.

---

## Bill of Material
| Image | Component | Price (SEK) | Purpose |
|----------|---------|
| <img src="https://www.electrokit.com/cache/ba/700x700-product_41019_41019114_PICO-WH-HERO.jpg" alt="Raspberry Pi Pico W" width="100"> | Raspberry Pi Pico WH | [Function] |
| Breadboard | [Function] |
| USB cable | [Function] |
| Lab cable M/M, F/M | [Type used] |
| Digital temperature and humidity sensor DHT11 | [Optional] |
| TLV49645 SIP-3 Hall effect sensor digital | [Optional] |
| MCP9700 TO-92 Temperature sensor | [Optional] |
| Photoresistor CdS 4-7 kohm | [Optional] |
| LEDs | [Optional] |
| Carbon film resistors | [Optional] |
| Magnet Neo35 Ø5mm x 5mm | [Optional] |
| Tactile switch PCB 6x6x5mm black | [Optional] |

---

## Raspberry Pi Pico W setup
- Plug it into your computer while pressing the reboot button, then copy the .UF2 file into the pico.  
  More information here: https://micropython.org/download/RPI_PICO_W/
- Download VS Code, follow the tutorial here: https://code.visualstudio.com/download
- Then install the Python extension:

![Python Extension](assets/images/python.png)

- And install the MicroPico extension to run the pico files:

![MicroPico Extension](assets/images/micropico.png)


---

## Wiring
TODO: fritzing diagram

---

## Environmental Comfort Calculation  
Describe how environmental readings are interpreted.  
Include any calculations or logic used, for example:

- Real-feel calculation (temp + humidity)  + code snippets TODO:
- Rain detection pattern  
- Thresholds or categories used (e.g., Cold, Pleasant, Hot)

1. Simple real-feel formula:
``` python
comfort = temperature + 0.2 * humidity
```


---

## Transmitting Data
Explain how data moves through the system:

- How often data is collected (e.g., every 3 seconds)  
- Where it is stored (e.g., database, server)  
- What triggers data transmission  
- Optional automation (e.g., push notifications)

---

## Data Storage and Visualization  
### Storage  
- InfluxDB running in Docker (docker-compose.yml includes influxdb, telegraf, grafana).

### Visualization  
- Grafana dashboards display:
    - Current comfort
    - Past 24h trends
    - Star ratings over time
- Embedded in a simple static HTML page.
---

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
---

## 8. Useful Links  
- GitHub repo: https://github.com/hannaszalai/IoT-benchmonitor  
- Demo Youtube video: `[YouTube link]`