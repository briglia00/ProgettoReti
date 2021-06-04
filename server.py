#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 18 12:41:55 2021

@author: briglia
"""
import socket, time

nanoseconds = lambda: int(time.time()*1000000)

buffer = 1024
server_ip = '10.10.10.2'
server_mac = 'AA:94:9F:EF:19:DB'
gateway_ip='10.10.10.5'
gateway_mac = '1D:EA:29:EF:19:DB'
server_address=('localhost',5000)

print ('starting up on %s port %s' % server_address)

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(server_address)

serverSocket.listen(1)

while True:

    print ('\nwaiting to receive messages...')
    connectionSocket, addr = serverSocket.accept()
    
    data = connectionSocket.recv(buffer)
    time_recv = nanoseconds()
    
    received_message =  data.decode("utf-8")
    source_mac = received_message[0:17]
    destination_mac = received_message[17:34]
    source_ip = received_message[34:44]
    destination_ip =  received_message[44:54]
    time_sent = received_message[54:74]
    message = received_message[74:]
    
    time.sleep(2)
    time_result = time_recv - int(time_sent)
    print('\nThe packed received:\nSource MAC address: {},\nDestination MAC address: {}'.format(source_mac, destination_mac))
    print('Source IP address: {},\nDestination IP address: {}'.format(source_ip, destination_ip))
    print('The Packet (TCP) weights {} bytes and took {}ns to reach its destination.\nThe TCP Buffer size is {} bytes'.format(len(data), time_result, buffer))
    print('\n' + message)
    connectionSocket.close()
