# Lake Balaton Bench Logger
*“Find the best benches to relax by the lake!”*
![Lake Balaton Bench](assets/images/header.png)

---

## Overview  
Each summer, thousands of people circle Lake Balaton by bike or foot, seeking the perfect place to rest. But what makes a bench perfect? Is it the view, the temperature, the breeze, or the warm sun on your back?  
A small IoT device was placed under one of Balaton’s most iconic benches to find out. It senses when people sit, how warm and humid it is, and how much sun hits the bench. It even lets passersby select their score from 1-5 stars which adds to the total score. All the data flows into a colorful website, complete with real-time comfort ratings, weather alerts, and history graphs.  
Think of it as TripAdvisor for benches.

What problem does it solve?  
What data is collected, and how is it used?
![Map](assets/images/map.png)

---

## Sensors and Components Used  
| Component | Purpose |
|----------|---------|
| Raspberry Pi Pico WH | [Function] |
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

## 3. Environmental Comfort Detection  
Describe how environmental readings are interpreted.  
Include any calculations or logic used, for example:

- Real-feel calculation (temp + humidity)  
- Rain detection pattern  
- Thresholds or categories used (e.g., Cold, Pleasant, Hot)

---

## 4. Daily Summary  
What metrics are collected daily? Example metrics:

- Total number of interactions (e.g., people sitting)  
- Average comfort score  
---

## 5. Data Flow  
Explain how data moves through the system:

- How often data is collected (e.g., every 3 seconds)  
- Where it is stored (e.g., database, server)  
- What triggers data transmission  
- Optional automation (e.g., push notifications)

---

## 6. Data Storage and Visualization  
### Storage  
- Platform used 
- Pros and cons  
- Any technical notes or issues encountered

### Visualization  
- Tools/libraries used 
- Realtime or static?  
- Custom UI or platform-based visualization?

---

## 7. Development Phases  
Outline the project in phases:

1. Phase 1 – Terminal output (basic testing)  
2. Phase 2 – Platform visualization (InfluxDB, Node-RED, etc.)  
3. Phase 3 – Custom website with graphs and live data

---

## 8. Useful Links  
- GitHub repo: `[link]`  
- Demo video: `[YouTube link]`  
- Data platform: `[InfluxDB or dashboard link]`  
