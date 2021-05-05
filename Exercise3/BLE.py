# Pysense 2.0
import machine
import network
import time
import pycom
from pycoproc_2 import Pycoproc

from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE

from network import Bluetooth
import ubinascii

BLEconnected = False

# handeler for Bluetooth connection
def connectionCallback(e):
    events = e.events()
    global BLEconnected
    if events & BLE.CLIENT_CONNECTED:
        BLEconnected = True
        print("Client connected")
    elif events & BLE.CLIENT_DISCONNECTED:
        BLEconnected = False
        print("Client disconnected")


def char1_cb_handler(chr, data):
    events, value = data
    if events & BLE.CHAR_WRITE_EVENT:
        print("Write request")
        pycom.rgbled(int.from_bytes(bytearray(value), 'big'))
    elif events & BLE.CHAR_READ_EVENT:
        print("Read Request")


pycom.heartbeat(False)

BLE = Bluetooth()

# initialize a BLE GATT server
BLE.set_advertisement(name='FiPy', service_uuid = b'19247847hfjs9h28')

Bluetooth().callback(trigger=BLE.CLIENT_CONNECTED | BLE.CLIENT_DISCONNECTED,
                     handler=connectionCallback)

BLE.advertise(True) # advertising its availability


# GATT services
srv1 = BLE.service(uuid= 0x100, isprimary = True, start=True)

# GATT characteristics
chr1 = srv1.characteristic(uuid = 0x101, properties=BLE.PROP_INDICATE |
                           BLE.PROP_BROADCAST | BLE.PROP_NOTIFY)

chr1.callback(trigger = BLE.CHAR_WRITE_EVENT, handler=char1_cb_handler)


py = Pycoproc()
# reading lux
lt = LTR329ALS01(py)

while(True):
    lux = lt.lux()
    #print("Light (lux): " + str(lux))
    hex_value = int(hex(int(lux)*10000))
    if BLEconnected:
    	chr1.value(str(lux))

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
