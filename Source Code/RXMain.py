import socket
from appR import *
import time
from RXfun import tahoe_congestion_control, filepath

ip = ""
port = ""
sock = None
address_port = None
buffer_size = 1024



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
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 64000 * 32)
        address_port = (ip,port)
        sock.bind(address_port)
        window.CONSOLE.append('Address : {}\n'.format(address_port))
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


def ConsoleAppendText(window,text):
    window.CONSOLE.append(text + "\n")
    window.CONSOLE.repaint()



def Reception(window):
    ConsoleAppendText(window,'Incepem bucla de receptie...')
    time.sleep(1)

    tahoe_congestion_control(window,sock,address_port,buffer_size)

    time.sleep(1)
    ConsoleAppendText(window,'Sfarsitul receptiei...')



class Ui_Interface(Ui_MainWindow):
    def __init__(self,window):
        self.setupUi(window)

    def SetActions(self):
        self.IP_OK.clicked.connect(lambda : setIp(self,self.IP.toPlainText()))
        self.PORT_OK.clicked.connect(lambda : setPort(self,self.PORT.toPlainText()))
        self.CREARESOCKET.clicked.connect(lambda : self.CREARESOCKETSTATUS.setText(creareSocket(self)))
        self.BROWSE_FILE.clicked.connect(lambda: BrowseFile(self))
        self.START.clicked.connect(lambda: Reception(self))

