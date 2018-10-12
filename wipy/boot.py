from network import WLAN

import pycom
import usocket
import machine

pycom.heartbeat(False)

wlan = WLAN(mode=WLAN.STA)
hote = "35.227.29.146"

nets = wlan.scan()
for net in nets:
    if net.ssid == 'honor':
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, 'sebsebseb'), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded on network : ' + net.ssid)
        break

    if net.ssid == 'GSWIOT':
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, 'IOT4GroupeSeb'), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded on network : ' + net.ssid)
        break

    if net.ssid == 'Freebox-B191BD':
        print('Network found!')
        wlan.connect(net.ssid,
        auth=(net.sec, 'cunabula-nitrea-indictivis*-procero79'), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded on network : ' + net.ssid)
        break
