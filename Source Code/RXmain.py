import socket
import time

from RXfun import *

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # ipv4, UDP
address_port = ("127.0.0.1", 5005)
buffer_size = 1024  # pachetul va contine 512B

sock.bind(address_port)

sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 64000 * 32)

i = 0
print('Incepem bucla de receptie..')
time.sleep(1)

tahoe_congestion_control(sock,address_port,buffer_size)

#file_write.close()
time.sleep(1)
print('\nReceptia a luat sfarsit.')
a = input('')


