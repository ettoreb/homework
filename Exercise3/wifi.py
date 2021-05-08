# Pysense 2.0
import machine
import network
import time
import pycom

from pycoproc_2 import Pycoproc
from LTR329ALS01 import LTR329ALS01 # lux sensor


pycom.heartbeat(False)
from network import WLAN
wlan = WLAN()

py = Pycoproc()
# reading lux
lt = LTR329ALS01(py)

import usocket
# establish standard IP socket
socket = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM, usocket.IPPROTO_TCP)
# Bound socket to local IP and random port
socket.bind((wlan.ifconfig()[0],100))
# Prints IP and Port number to be used by Putty.
print("IP address " + str(wlan.ifconfig()[0]) + ", Port " + str(100))
print("Listening for connection")
# Listen on socket for incoming connection
socket.listen()
# Accepts latest connection and gets socket object
LUX_value = socket.accept()[0]
print("Connection accepted")

while(True):
    lux = lt.lux()
    #print("Light (lux): " + str(lux))
    hex_value = int(hex(int(lux)*10000))
    LUX_value.send(str(lux) + " lux" + "\r\n") # Send lux status

    # Switch on a Led selecting a color from a graduated scale
    if lux in range(0,500):
        pycom.rgbled(0xf00000)
    elif lux in range(500,800):
        pycom.rgbled(0x0000f0)
    elif lux in range(800,1000):
        pycom.rgbled(0x00f000)
    elif lux in range(1000,1500):
        pycom.rgbled(0x0f0000)
    elif lux in range(1500,2000):
        pycom.rgbled(0xffffff)


    time.sleep(1)
