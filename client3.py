#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 19 11:18:16 2021

@author: briglia
"""
import socket, time, random
from datetime import datetime

nanoseconds = lambda: int(time.time()*1000000)

client3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client3_ip = "192.168.1.17"
client3_mac = "AF:04:67:EF:19:DA"
temp = 7
hum = 19
timer = 24*60*60 #24 ore
router_ip = '192.168.1.20'
router_mac = '05:10:0A:CB:24:EF'
router_address = ('localhost', 5200)

IP_header = '' + client3_ip + router_ip
ethernet_header = '' + client3_mac + router_mac

while True:
    
    print ('smart meter 3 is sending message...')
    now = datetime.now()
    now = now.strftime("%H:%M:%S")
    temp = temp + random.randint(-3,3)
    hum = hum + random.randint(-3,3)
    if hum < 0:
        hum = 0
    message = '{:020d} - {} - {}C - {}%'.format(nanoseconds(), now, temp, hum)

    packet = ethernet_header + IP_header + message
    sent = client3.sendto(packet.encode('utf-8'), router_address)
    print ('sent {} bytes to gateway at IP address {}'.format(sent, router_ip))
    time.sleep(timer)
