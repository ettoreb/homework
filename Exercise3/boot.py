# Exercise 3 - Innovative Wireless Platform for Internet of Things
# Politecnico di Torino
# Ettore Bartoli s277157

import pycom
from network import WLAN
import machine

pycom.pybytes_on_boot(False) #we do not want Pybytes using the WLAN
pycom.smart_config_on_boot(False) #we also do not want smart config
pycom.wifi_on_boot(True)
pycom.wifi_mode_on_boot(WLAN.STA)
pycom.wifi_ssid_sta('network_ssid')
pycom.wifi_pwd_sta('network_password')

#machine.main('wifi.py')
machine.main('BLE.py')
