import pycom
import machine
import time
from network import WLAN

# TX Power levels
levels = {
  1:
    {
      "level" : "level 0",
      "range" : range(78,127),
      "led"   : 0x00000f
    },
  2:
    {
      "level" : "level 1",
      "range" : range(76,77),
      "led"   : 0x0000f0
    },
  3:
    {
      "level" : "level 2",
      "range" : range(74,75),
      "led"   : 0x000f00
    },
  4:
    {
      "level" : "level 3",
      "range" : range(68,73),
      "led"   : 0x00f000
    },
  5:
    {
      "level" : "level 4",
      "range" : range(60,67),
      "led"   : 0x0f0000
    },
  6:
    {
      "level" : "level 5",
      "range" : range(52,59),
      "led"   : 0xf00000
    },
  7:
    {
      "level" : "level5 - 2dBm",
      "range" : range(44,51),
      "led"   : 0x000000
    },
  8:
    {
      "level" : "level5 - 4.5dBm",
      "range" : range(34,43),
      "led"   : 0xffffff
    },
  9:
    {
      "level" : "level5 - 6dBm",
      "range" : range(28,33),
      "led"   : 0x0f0010
    },
  10:
    {
      "level" : "level5 - 8dBm",
      "range" : range(20,27),
      "led"   : 0x0a0011
    },
  11:
    {
      "level" : "level5 - 11dBm",
      "range" : range(8,19),
      "led"   : 0x0b0012
    },
  0:
    {
      "level" : "level5 - 14dBm",
      "range" : range(-128,7),
      "led"   : 0x0c0013
    }

}


wlan = WLAN()

if machine.reset_cause() != machine.SOFT_RESET:
    wlan.init(mode=WLAN.STA)
    wlan.ifconfig(config=(
        '192.168.1.128',    #ip
        '255.255.255.0',    #subnet_mask
        '192.168.1.254',    #gateway
        '8.8.8.8'))         #DNS_server
ssid = wlan.ssid()
ch = wlan.channel()
print("connected to "+ str(ssid))
print("channel "+ str(ch)) # read the channel

# signal level
tx_power = wlan.max_tx_power()

# light a selecting a color from a
# graduated scale associated to signal possible ranges
for k in range(len(levels)):
    if tx_power in levels[k]["range"]:
        print(levels[k]["level"]) # signal level
        pycom.rgbled(levels[k]["led"])
