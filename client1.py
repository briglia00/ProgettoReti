#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 19 11:18:16 2021

@author: briglia
"""
import socket, time, random
from datetime import datetime

nanoseconds = lambda: int(time.time()*1000000)

client1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client1_ip = "192.168.1.15"
client1_mac = "32:04:0A:EF:19:CF"
temp = 15
hum = 10
timer = 24*60*60 #24 ore
router_ip = '192.168.1.20'
router_mac = '05:10:0A:CB:24:EF'
router_address = ('localhost', 5200)

IP_header = '' + client1_ip + router_ip
ethernet_header = '' + client1_mac + router_mac

while True:
    
    print ('smart meter 1 is sending message...')
    now = datetime.now()
    now = now.strftime("%H:%M:%S")
    temp = temp + random.randint(-3,3)
    hum = hum + random.randint(-3,3)
    if hum < 0:
        hum = 0
    message = '{:020d} - {} - {}C - {}%'.format(nanoseconds(), now, temp, hum)

    packet = ethernet_header + IP_header + message
    sent = client1.sendto(packet.encode('utf-8'), router_address)
    print ('sent {} bytes to gateway at IP address {}'.format(sent, router_ip))
    time.sleep(timer)
