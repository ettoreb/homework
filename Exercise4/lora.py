from network import LoRa
import socket
import pycom
import ubinascii

# Initialise LoRa in LORAWAN mode
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
# device unique identifier
print("device EUI: " + ubinascii.hexlify(lora.mac()).upper().decode('utf-8'))

# create an OTAA authentication parameters
dev_eui = ubinascii.unhexlify('70B3D54990DC335F') #bytes
app_eui = ubinascii.unhexlify('70B3D57ED0042649')
app_key = ubinascii.unhexlify('A6F0ABCD828E323E7F7300E86ECE72AC')

# starting a join sequence
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    print('Not yet joined...')

print('Joined Network')


# create a raw LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
# configure data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
# make the socket blocking
s.setblocking(True)

#define a port
s.bind(2)

# send data
s.send(bytes([0x01,0x02]))
s.setblocking(False)

# get data
data_RX = s.recv(64)
#print("data received: "+data_RX)


frequency = lora.frequency()
frequency = frequency/10000000
print("frequency = "+ str(frequency) +"GHz")


stats = lora.stats()
#get the power of the last transmission
tx_power = stats[6] # signal level
print("tx power level: " + tx_power +" dBm")

# light a selecting a color from a graduated scale associated to signal possible ranges
if tx_power in range(0, 10):
    pycom.rgbled(0x7f0000) # red
elif tx_power in range(10, 20):
    pycom.rgbled(0x007f00) # green
elif tx_power in range(20,30):
    pycom.rgbled(0x7f7f00) # yellow
else:
    pycom.rgbled(0xffffff) #
