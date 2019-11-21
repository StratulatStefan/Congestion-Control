import socket
from TXfun import *

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # ipv4, UDP

address_port = ("127.0.0.1", 5005)
file_name_to_send = "fisier.txt"

segment = encode('START', file_name_to_send)
sock.sendto(segment, address_port)

for segment in encode_bytes(file_name_to_send):
    sock.sendto(segment, address_port)

# sock.sendto(("Mesaj trimis").encode("UTF-8"), address_port)





