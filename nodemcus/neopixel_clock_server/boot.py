# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc, webrepl, network
import ujson as json

import neopixel, machine

webrepl.start()

# Disable access point. Don't need so many WIFIs.
ap_if = network.WLAN(network.AP_IF)
if ap_if.active():
    ap_if.active(False)

sta_if = network.WLAN(network.STA_IF)
if not sta_if.active():
    sta_if.active(True)
    
available_networks = sta_if.scan()

with open("networks.json", "r") as f:
    network_data = json.load(f)
for network in available_networks:
    network_name = network[0].decode()
    if network_name in network_data.keys():
        sta_if.connect(network_name, network_data[network_name])
        break

with open("neopixels.json", "r") as f:
    neopixels = json.load(f)

number_of_leds =  neopixels["number_of_leds"]
np = neopixel.NeoPixel(machine.Pin(neopixels["pin"]), number_of_leds) 
for i in range(number_of_leds):
    np[i] = (0,0,0)
np.write()
gc.collect()
