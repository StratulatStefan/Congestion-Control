import socket
import time
import threading
from transmitter_ui import *

class NetworkHandler:
    def __init__(self):
        pass

    def setIp(self,window,transmitter,ui_ip):
        transmitter.ip = ui_ip
        window.ConsoleAppendText(f'IP : {transmitter.ip}\n',0)


    def setPortRX(self,window,transmitter,ui_port):
        transmitter.port_RX = int(ui_port)
        window.ConsoleAppendText(f'Port RX: {transmitter.port_RX}\n',0)


    def setPortTX(self,window,transmitter,ui_port):
        transmitter.port_TX = int(ui_port)
        window.ConsoleAppendText(f'Port TX: {transmitter.port_TX}\n',0)

    def creareSocket(self,window,transmitter):
        try:
            transmitter.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            transmitter.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 64000 * 32)
            transmitter.address_RX = (transmitter.ip,transmitter.port_RX)
            transmitter.address_TX = (transmitter.ip,transmitter.port_TX)
            transmitter.sock.bind(transmitter.address_RX)
            window.ConsoleAppendText(f'Address RX : {transmitter.address_RX}\n',0)
            window.ConsoleAppendText(f'Address TX : {transmitter.address_TX}\n',0)
        except socket.error:
            return 'Eroare la crearea socket-ului'
        else:
            return 'Socket creat cu succes'

    def BrowseFile(self,window,transmitter):
        primary_file_path = "D:\\\Learning\\\RC\\input\\"
        transmitter.filepath,_filter = QFileDialog.getOpenFileName(None,"Open File",primary_file_path)
        window.SELECTFILE_TEXT.setText(transmitter.filepath)


    def Transmission(self,window,transmitter):
        window.ConsoleAppendText('Incepem bucla de transmisie...',0)
        time.sleep(0.5)

        window.ConsoleAppendText('Incepem transmisia pachetelor de date..',0)


        threading.Thread(target=transmitter.tahoe_congestion_control,args = (window,)).start()
