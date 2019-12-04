import socket
import time
from RXfun import *


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # ipv4, UDP
address_port = ("127.0.0.1", 5005)
buffer_size = 1024  # pachetul va contine 512B

sock.bind(address_port)



print('Incepem bucla de receptie..')
time.sleep(2)
while True:
    data, addr = sock.recvfrom(buffer_size)


    decoded_data = SegmentDecode(data)
    if decoded_data['tip'] == 1:
        print('A fost generat pachetul de start..')
        time.sleep(2)
        file_name = FileNameDecode(decoded_data['data'],decoded_data['len'])
        print('Numele fisierului : ',file_name)
        time.sleep(1)
        file_write = open(file_name,'wb')
        print('Fisierul a fost creat cu succes..')
    elif decoded_data['tip'] == 3:
        time.sleep(2)
        print('\n\nReceptia a luat sfarsit deoarece a fost transmit pachetul final...')
        time.sleep(2)
        file_write.write(decoded_data['data'])
        break

print('Gata..')



