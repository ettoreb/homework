from network import LoRa
import socket
import pycom

# Initialize LoRa in LORA mode.

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)

# create a raw LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)

frequency = lora.frequency()
frequency = frequency/10000000
print("frequency = "+ str(frequency) +"GHz")


stats = lora.stats()
tx_power = stats[6] # signal level

# light a selecting a color from a graduated scale associated to signal possible ranges
if tx_power in range(0, 10):
    pycom.rgbled(0x7f0000) # red
elif tx_power in range(10, 20):
    pycom.rgbled(0x007f00) # green
elif tx_power in range(20,30):
    pycom.rgbled(0x7f7f00) # yellow
else:
    pycom.rgbled(0xffffff) #
