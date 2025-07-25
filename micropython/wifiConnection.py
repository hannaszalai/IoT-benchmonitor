import network
from time import sleep

SSID = "Vodafone-C931"
PASSWORD = "sKtHQ5Wjnkx8wndd"

# Connects to WiFi and returns the IP address.
def connect():
    wlan = network.WLAN(network.STA_IF)         # Put modem on Station mode
    if not wlan.isconnected():                  # Check if already connected
        print('connecting to network...')
        wlan.active(True)                       # Activate network interface
        # set power mode to get WiFi power-saving off (if needed)
        wlan.config(pm = 0xa11140)
        wlan.connect(SSID, PASSWORD)  # Your WiFi Credential
        print('Waiting for connection...', end='')
        # Check if it is connected otherwise wait
        while not wlan.isconnected() and wlan.status() >= 0:
            print('.', end='')
            sleep(1)
    # Print the IP assigned by router
    ip = wlan.ifconfig()[0]
    print('\nConnected on {}'.format(ip))
    return ip

# Disconnects from WIFI.
def disconnect():
    wlan = network.WLAN(network.STA_IF)   # Put modem on Station mode
    wlan.disconnect()
    wlan = None 