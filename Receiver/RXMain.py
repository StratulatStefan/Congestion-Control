import socket
import threading
from  receiver_ui import *
from RXfun import *

ip = "127.0.0.1"
portRX = 5005
portTX = 4004
sock = None
address_port_TX = None
address_port_RX = None
buffer_size = 512 + 8
loss_probability = None


def setIp(window,ui_ip):
    global ip
    ip = ui_ip
    ConsoleAppendText(window,'IP : {}\n'.format(ip))

def setPortRX(window,ui_port):
    global portRX
    portRX = int(ui_port)
    ConsoleAppendText(window,'Port RX: {}\n'.format(portRX))

def setPortTX(window,ui_port):
    global portTX
    portTX = int(ui_port)
    ConsoleAppendText(window,'Port TX: {}\n'.format(portTX))

def setLossProbability(window,probability):
    global loss_probability
    loss_probability = int(probability)
    ConsoleAppendText(window,'Probabilitate pierdere pachete : {}\n'.format(loss_probability))

def creareSocket(window):
    global ip
    global port
    global sock
    global address_port_TX
    global address_port_RX
    try:
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 64000 * 32)
        address_port_RX = (ip,portRX)
        address_port_TX = (ip,portTX)
        sock.bind(address_port_RX)
        ConsoleAppendText(window,'Address RX : {}\n'.format(address_port_RX))
        ConsoleAppendText(window,'Address TX : {}\n'.format(address_port_TX))
    except socket.error:
        return 'Eroare la crearea socket-ului'
    else:
        return 'Socket creat cu succes'


def BrowseFile(window):
    global number_of_chunks
    global filepath
    primary_file_path = "D:\\\Learning\\\RC\\input\\"
    filepath = QFileDialog.getExistingDirectory(None,"Select Output Folder",primary_file_path)
    window.SELECTFILE_TEXT.setText(filepath)



def Reception(window):
    global sock
    global tahoe_thread
    ConsoleAppendText(window,'Incepem bucla de receptie...')
    time.sleep(1)


    tahoe_thread = threading.Thread(target=tahoe_congestion_control,args=(window,sock,address_port_TX,buffer_size,loss_probability))
    tahoe_thread.start()




class Ui_Interface(Ui_MainWindow):
    def __init__(self,window):
        self.setupUi(window)

    def SetActions(self):
        self.IP_OK.clicked.connect(lambda : setIp(self,self.IP.toPlainText()))
        self.PORT_OK_RX.clicked.connect(lambda : setPortRX(self,self.PORT_RX.toPlainText()))
        self.PORT_OK_TX.clicked.connect(lambda : setPortTX(self,self.PORT_TX.toPlainText()))
        self.PORT_OK_PPP.clicked.connect(lambda : setLossProbability(self,self.LABEL_PPP.toPlainText()))
        self.CREARESOCKET.clicked.connect(lambda : self.CREARESOCKETSTATUS.setText(creareSocket(self)))
        self.BROWSE_FILE.clicked.connect(lambda: BrowseFile(self))
        self.START.clicked.connect(lambda: Reception(self))

