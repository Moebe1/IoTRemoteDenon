# This file is executed on every boot (including wake-boot from deepsleep)

#import esp

#esp.osdebug(None)

import gc
import os

#import webrepl

#webrepl.start()

gc.collect()

import time
from simple import MQTTClient
import simple
import ubinascii
import machine
import micropython
import network
import esp
esp.osdebug(None)
import gc
import time

from rotary_irq_esp import RotaryIRQ
gc.collect()

ssid = 'OPTUSVD388E5E8'
password = 'PROWSMACON17146'
mqtt_server = '192.168.0.12'
#EXAMPLE IP ADDRESS

#mqtt_server = '192.168.1.144'
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'notification'
topic_pub = b'denon'

last_message = 0
message_interval = 5
counter = 0

AccessPoint = network.WLAN(network.AP_IF)
AccessPoint.active(False)
station = network.WLAN(network.STA_IF)
station.config(dhcp_hostname="DenonIoTRemote")
station.active(True)

station.connect(ssid, password)

while station.isconnected() == False:
  pass
print('Connection successful')
print(station.ifconfig())