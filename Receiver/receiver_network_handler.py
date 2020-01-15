import socket
import time
import threading
from  receiver_ui import *
buffer_size = 512 + 8


class NetworkHandler:
    def __init__(self):
        pass

    def setIp(self,window,receiver,ui_ip):
        receiver.ip = ui_ip
        window.ConsoleAppendText(f'IP : {receiver.ip}\n')


    def setPortRX(self,window,receiver,ui_port):
        receiver.port_RX = int(ui_port)
        window.ConsoleAppendText(f'Port RX: {receiver.port_RX}\n')


    def setPortTX(self,window,receiver,ui_port):
        receiver.port_TX = int(ui_port)
        window.ConsoleAppendText(f'Port TX: {receiver.port_TX}\n')

    def setLossProbability(self,window,receiver,probability):
        receiver.loss_probability = int(probability)
        window.ConsoleAppendText(f'Probabilitate pierdere pachete : {receiver.loss_probability}\n')

    def creareSocket(self,window,receiver):
        try:
            receiver.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            receiver.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 64000 * 32)
            receiver.address_RX = (receiver.ip,receiver.port_RX)
            receiver.address_TX = (receiver.ip,receiver.port_TX)
            receiver.sock.bind(receiver.address_RX)
            window.ConsoleAppendText(f'Address RX : {receiver.address_RX}\n')
            window.ConsoleAppendText(f'Address TX : {receiver.address_TX}\n')
        except socket.error:
            return 'Eroare la crearea socket-ului'
        else:
            return 'Socket creat cu succes'


    def BrowseFile(self,window,receiver):
        primary_file_path = "D:\\\Learning\\\RC\\input\\"
        receiver.filepath = QFileDialog.getExistingDirectory(None,"Select Output Folder",primary_file_path)
        window.SELECTFILE_TEXT.setText(receiver.filepath)

    def Reception(self,window,receiver):
        global buffer_size
        window.ConsoleAppendText('Incepem bucla de receptie...')
        time.sleep(1)

        threading.Thread(target=receiver.tahoe_congestion_control,args=(window,buffer_size)).start()