import pycom
import network

from network import WLAN

server = network.Server()
pycom.heartbeat(False)

wlan = WLAN()

if wlan.isconnected():
    print("connected to the network: " + wlan.ssid())
    pycom.rgbled(0x007f00) # green
else:
    pycom.rgbled(0x7f0000) # red
