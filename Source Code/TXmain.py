import socket
import time
from TXfun import *

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # ipv4, UDP

address_port = ("127.0.0.1", 5005)
file_name_to_send = "file.txt"



print('Incepem bucla de transmisie...')
time.sleep(2)

print('Trimitem pachetul de start...')
time.sleep(1)
segment = encode('START', file_name_to_send)
sock.sendto(segment, address_port)

'''

'''


for segment in encode_bytes(file_name_to_send):
    sock.sendto(segment, address_port)

print('Trimitem pachetul de stop...')
time.sleep(1)
segment = encode('END','')
sock.sendto(segment, address_port)

print('Gta...')
a = input('')