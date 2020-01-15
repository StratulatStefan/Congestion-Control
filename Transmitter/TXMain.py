import socket
from transmitter_ui import *
from TX_fun_tahoe import *

ip = "127.0.0.1"
portRX = 4004
portTX = 5005
sock = None
address_port_RX = None
address_port_TX = None
filepath = ""


def setIp(window,ui_ip):
    global ip
    ip = ui_ip
    ConsoleAppendText(window,'IP : {}\n'.format(ip),0)

def setPortRX(window,ui_port):
    global portRX
    portRX = int(ui_port)
    ConsoleAppendText(window,'Port RX: {}\n'.format(portRX),0)

def setPortTX(window,ui_port):
    global portTX
    portTX = int(ui_port)
    ConsoleAppendText(window,'Port TX: {}\n'.format(portTX),0)

def creareSocket(window):
    global ip
    global port
    global sock
    global address_port_RX
    global address_port_TX
    try:
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        address_port_RX = (ip,portRX)
        address_port_TX = (ip,portTX)
        sock.bind(address_port_RX)
        ConsoleAppendText(window,'Address RX : {}\n'.format(address_port_RX),0)
        ConsoleAppendText(window,'Address TX : {}\n'.format(address_port_TX),0)
    except socket.error:
        return 'Eroare la crearea socket-ului'
    else:
        return 'Socket creat cu succes'


def BrowseFile(window):
    global filepath
    global number_of_chunks
    primary_file_path = "D:\\\Learning\\\RC\\input\\"
    filepath,_filter = QFileDialog.getOpenFileName(None,"Open File",primary_file_path)
    window.SELECTFILE_TEXT.setText(filepath)


def Transmission(window):
    global tahoe_thread
    ConsoleAppendText(window,'Incepem bucla de transmisie...',0)
    time.sleep(0.5)

    ConsoleAppendText(window,'Incepem transmisia pachetelor de date..',0)


    tahoe_thread = threading.Thread(target=tahoe_congestion_control,args = (window,sock,address_port_TX,filepath))
    tahoe_thread.start()


class Ui_Interface(Ui_MainWindow):
    def __init__(self,window):
        self.setupUi(window)

    def SetActions(self):
        self.IP_OK.clicked.connect(lambda : setIp(self,self.IP.toPlainText()))
        self.PORT_OK_RX.clicked.connect(lambda : setPortRX(self,self.PORT_RX.toPlainText()))
        self.PORT_OK_TX.clicked.connect(lambda : setPortTX(self,self.PORT_TX.toPlainText()))
        self.CREARESOCKET.clicked.connect(lambda : self.CREARESOCKETSTATUS.setText(creareSocket(self)))
        self.BROWSE_FILE.clicked.connect(lambda: BrowseFile(self))
        self.START.clicked.connect(lambda: Transmission(self))

