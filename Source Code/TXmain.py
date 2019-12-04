import socket
import time
from TXfun import *

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # ipv4, UDP

sock.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_SNDBUF,
    64000 * 16)

address_port = ("127.0.0.1", 5005)
#file_name_to_send = "verisign.bmp" #merge
#file_name_to_send = "main.py"     #merge
#file_name_to_send = "file.txt"    #merge
#file_name_to_send = "AiMultiChannel.prj" #merge
#file_name_to_send = "ghid.pdf" #nu merge
#file_name_to_send = "extra.png" #nu merge
#file_name_to_send = "image.jpg" #nu prea merge, o cam strica in proportie de 60%
#file_name_to_send = "archive.zip" #merge cu unexpected end of archive
file_name_to_send = "extras.png"

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
'''
print('Trimitem pachetul de stop...')
time.sleep(1)
segment = encode('END','')
sock.sendto(segment, address_port)
'''
print('Gta...')
a = input('')