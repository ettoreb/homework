from network import Sigfox
import socket
import struct
import time

# init Sigfox for RCZ1 (Europe)
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)

# create a Sigfox socket
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)

# make the socket blocking
s.setblocking(True)

# configure it as uplink only
s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)

# send some bytes
s.send("Hello SigFox")

freq=sigfox.frequencies()
print("uplink frequency = "+ str(freq[0]/10000000) + " GHz")
print("downlink frequency = "+ str(freq[1]/10000000) + " GHz")

# await DOWNLINK message
#downlink_message = s.recv(32)
#print(ubinascii.hexlify(downlink_message))


# signal downlink level
r = sigfox.rssi()

# light a selecting a color from a graduated scale associated to signal possible ranges
import pycom
if r in range(0, 10):
    pycom.rgbled(0x7f0000) # red
elif r in range(10, 20):
    pycom.rgbled(0x007f00) # green
elif r in range(20,30):
    pycom.rgbled(0x7f7f00) # yellow
else:
    pycom.rgbled(0xffffff) # white

# print signal level
print("downlink signal level: " + str(r))
time.sleep(2)
pycom.heartbeat(False)
