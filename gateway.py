#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 18 11:07:57 2021

@author: briglia
"""

import socket, time

nanoseconds = lambda: int(time.time()*1000000)

def gateway_send(ethernet_header, ip_header, msg, server_address):
    gateway_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    gateway_send.connect(server_address)
    
    print("\nserver connected!")
    packet = '{}{}{:20d}{}'.format(ethernet_header, ip_header,nanoseconds(), msg)
    sent = gateway_send.send(packet.encode('utf-8'))
    print ('sent %s bytes to %s' % (sent, 'server at IP address ' + server_ip + '\n'))
    gateway_send.close()

gateway = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
gateway_receive_ip = '192.168.1.20'
gateway_send_ip = '10.10.10.5'
gateway_mac = '1D:EA:29:EF:19:DB'
gateway_addr = ('localhost', 5200)
server_ip = '10.10.10.2'
server_mac = 'AA:94:9F:EF:19:DB'
server_addr = ('localhost', 5000)

client1_ip = "192.168.1.15"
client1_mac = "32:04:0A:EF:19:CF"
client2_ip = "192,168.1.16"
client2_mac = "10:AF:CB:EF:19:CF"
client3_ip = "192.168.1.17"
client3_mac = "AF:04:67:EF:19:DA"
client4_ip = "192.168.1.18"
client4_mac = "B0:F4:21:EF:19:DA"

buffer = 1024

client1 = None
client2 = None
client3 = None
client4 = None

arp_table_mac = {client1_ip : client1_mac, client2_ip : client2_mac, client3_ip : client3_mac, client4_ip : client4_mac}

IP_header = '' + gateway_send_ip + server_ip
ethernet_header = '' + gateway_mac + server_mac

print ('starting up on %s port %s' % gateway_addr)
gateway.bind(gateway_addr)

request = ''

while True:
    print('\nWaiting to receive message...')
    data, address = gateway.recvfrom(buffer)
    time_recv = nanoseconds()
         
    received_message = data.decode("utf-8")
    source_mac = received_message[0:17]
    destination_mac = received_message[17:34]
    source_ip = received_message[34:46]
    destination_ip = received_message[46:58]
    time_result = time_recv - int(received_message[58:78])
    message = received_message[78:]
    
    print('The Packet (UDP) weights {} bytes and took {}ns to reach its destination.\nThe UDP Buffer size is {} bytes'.format(len(data), time_result, buffer))
    
    if(client1 == None and source_ip == client1_ip and source_mac == client1_mac):
        client1 = address
        request = request + client1_ip + message + '\n'
    elif(client2 == None and source_ip == client2_ip and source_mac == client2_mac):
        client2 = address
        request = request + client2_ip + message + '\n'
    elif(client3 == None and source_ip == client3_ip and source_mac == client3_mac):
        client3 = address
        request = request + client3_ip + message + '\n'
    elif(client4 == None and source_ip == client4_ip and source_mac == client4_mac):
        client4 = address
        request = request + client4_ip + message + '\n'
    else:
        continue
    
    print('\nThe packed received:\nSource MAC address: {},\nDestination MAC address: {}'.format(source_mac, destination_mac))
    print('Source IP address: {},\nDestination IP address: {}\n'.format(source_ip, destination_ip))

    if (client1 != None and client2 != None and client3 != None and client4 != None):
        gateway.close()
        
        arp_table_socket = {client1_ip : client1, client2_ip : client2, client3_ip : client3, client4_ip : client4}
        
        print('\nSending data to the Server...')
        gateway_send(ethernet_header, IP_header, request, server_addr)
        
        client1 = None; client2 = None; client3 = None; client4 = None; request = ''
        gateway = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        gateway.bind(gateway_addr)
        

