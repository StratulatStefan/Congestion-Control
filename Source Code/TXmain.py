import socket
import time
from TXfun import *

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # ipv4, UDP

address_port = ("127.0.0.1", 5005)
# file_name_to_send = "input//verisign.bmp"             #merge
# file_name_to_send = "input//AiMultiChannel.prj"       #merge
# file_name_to_send = "input//ghid.pdf"                 #merge
# file_name_to_send = "input//extra.png"                #merge
# file_name_to_send = "input//image.jpg"                #merge
# file_name_to_send = "input//archive.zip"              #merge
# file_name_to_send = "input//extras.png"               #merge
# file_name_to_send = "input//icon.png"                 #merge
# file_name_to_send = "input//LAND3.bmp"                #merge
# file_name_to_send = "input//tanc.jpg"                 #merge
# file_name_to_send = "input//bohemian-rapsody.mp3"     #merge (are 9MB)
# file_name_to_send = "input//main.py"                  #merge
file_name_to_send = "input//giphy.gif"                 #merge


print('Incepem bucla de transmisie...')
time.sleep(2)

print('Trimitem pachetul de start...')
time.sleep(1)
segment = encode('START', file_name_to_send)
sock.sendto(segment, address_port)


for segment in encode_bytes(file_name_to_send):
    # print("\n\n")
    sock.sendto(segment, address_port)

print('Gata...')
a = input('')