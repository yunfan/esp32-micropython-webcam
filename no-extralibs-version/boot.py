
import network

SID = 'your wifi ap'
PASS = 'your wifi password'

def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.config(dhcp_hostname='esp32cam')
        wlan.connect(SID, PASS)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

do_connect()

import webcam
webcam.start()
