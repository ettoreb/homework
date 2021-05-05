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


BLE = Bluetooth()

# initialize a BLE GATT server
BLE.set_advertisement(name='FiPy', service_uuid = b'19247847hfjs9h28')
Bluetooth().callback(trigger=BLE.CLIENT_CONNECTED | BLE.CLIENT_DISCONNECTED,
                     handler=connectionCallback)

print("start scanning..")
BLE.start_scan(-1)
#time.sleep_ms(2000)
while BLE.isscanning():
    advs = BLE.get_adv()
    if advs:
        BLE_ch = BLE.resolve_adv_data(advs.data, BLE.ADV_NAME_CMPL)
        BLE_rssi = advs.rssi
        if str(BLE_ch) != "None":
            print("Bluetooth channel: " + BLE_ch)
            print("rssi: " + BLE_rssi) # signal level
            BLE.stop_scan()
            pycom.heartbeat(False)

# turn on led
if BLE_rssi in range(0, 10):
    pycom.rgbled(0x7f0000) # red
elif BLE_rssi in range(10, 20):
    pycom.rgbled(0x007f00) # green
elif BLE_rssi in range(20,30):
    pycom.rgbled(0x7f7f00) # yellow
else:
    pycom.rgbled(0xffffff) # white
