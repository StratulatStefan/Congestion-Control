import socket
from TX_fun_tahoe import *

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # ipv4, UDP
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
address_port = ("127.0.0.1", 5005)
address_port_RX = ("127.0.0.1", 4004)
sock.bind(address_port_RX)


# file_name_to_send = "input//verisign.bmp"             #merge
# file_name_to_send = "input//AiMultiChannel.prj"       #merge
# file_name_to_send = "input//ghid.pdf"                 #merge
# file_name_to_send = "input//extra.png"                #merge
file_name_to_send = "input//image.jpg"                #merge
#file_name_to_send = "input//archive.zip"              #merge
# file_name_to_send = "input//extras.png"               #merge
# file_name_to_send = "input//icon.png"                 #merge
# file_name_to_send = "input//LAND3.bmp"                #merge
# file_name_to_send = "input//tanc.jpg"                 #merge
# file_name_to_send = "input//bohemian-rapsody.mp3"     #merge (are 9MB)
# file_name_to_send = "input//main.py"                  #merge
#file_name_to_send = "input//giphy.gif"                 #merge


print('Incepem bucla de transmisie...')
time.sleep(0.5)


tahoe_congestion_control(sock, address_port, file_name_to_send)
print('Am terminat de transmis primul fisier\n\n\n')
time.sleep(2)

file_name_to_send = "input//verisign.bmp"             #merge
tahoe_congestion_control(sock, address_port, file_name_to_send)
print('Am terminat de transmis al doilea fisier\n\n\n')
time.sleep(2)


#file_name_to_send = "input//bohemian-rapsody.mp3"     #merge (are 9MB)
#tahoe_congestion_control(sock, address_port, file_name_to_send)
#print('Am terminat de transmis al treilea fisier\n\n\n')

time.sleep(1)



print('\nSfarsitul transmisiei...')
