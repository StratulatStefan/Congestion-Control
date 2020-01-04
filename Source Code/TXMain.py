import socket
from app import *
from TXfun import *

ip = ""
port = ""
sock = None
address_port = None
filepath = ""

def setIp(window,ui_ip):
    global ip
    ip = ui_ip
    window.CONSOLE.append('IP : {}\n'.format(ip))

def setPort(window,ui_port):
    global port
    port = int(ui_port)
    window.CONSOLE.append('Port : {}\n'.format(port))

def creareSocket(window):
    global ip
    global port
    global sock
    global address_port
    try:
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        address_port = (ip,port)
        window.CONSOLE.append('Address : {}\n'.format(address_port))
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


def ConsoleAppendText(window,text):
    window.CONSOLE.append(text + "\n")
    window.CONSOLE.repaint()



def Transmission(window):
    ConsoleAppendText(window,'Incepem bucla de transmisie...')
    time.sleep(2)

    ConsoleAppendText(window,'Trimitem pachetul de start...')
    time.sleep(1)
    segment = encode('START',filepath)
    sock.sendto(segment,address_port)

    ConsoleAppendText(window,'A fost trimis pachetul de start...')
    time.sleep(1)
    ConsoleAppendText(window,'Incepem transmisia pachetelor de date..')
    tahoe_congestion_control(window,sock,address_port,filepath)

    time.sleep(1)
    ConsoleAppendText(window,'Pachetele de date au fost trimise...')

    time.sleep(1)
    ConsoleAppendText(window,'Sfarsitul transmisie...')



class Ui_Interface(Ui_MainWindow):
    def __init__(self,window):
        self.setupUi(window)

    def SetActions(self):
        self.IP_OK.clicked.connect(lambda : setIp(self,self.IP.toPlainText()))
        self.PORT_OK.clicked.connect(lambda : setPort(self,self.PORT.toPlainText()))
        self.CREARESOCKET.clicked.connect(lambda : self.CREARESOCKETSTATUS.setText(creareSocket(self)))
        self.BROWSE_FILE.clicked.connect(lambda: BrowseFile(self))
        self.START.clicked.connect(lambda: Transmission(self))

