import time
from threading import RLock
from transmitter_ui import *

class Ui_Interface(Ui_MainWindow):
    def __init__(self,window):
        self.console_lock = RLock()
        self.setupUi(window)

    def SetActions(self,transmitter):
        self.IP_OK.clicked.connect(
            lambda : transmitter.networkHandler.setIp(self,transmitter,self.IP.toPlainText())
        )
        self.PORT_OK_RX.clicked.connect(
            lambda : transmitter.networkHandler.setPortRX(self,transmitter,self.PORT_RX.toPlainText())
        )
        self.PORT_OK_TX.clicked.connect(
            lambda : transmitter.networkHandler.setPortTX(self,transmitter,self.PORT_TX.toPlainText())
        )
        self.CREARESOCKET.clicked.connect(
            lambda : self.CREARESOCKETSTATUS.setText(transmitter.networkHandler.creareSocket(self,transmitter))
        )
        self.BROWSE_FILE.clicked.connect(
            lambda: transmitter.networkHandler.BrowseFile(self,transmitter)
        )
        self.START.clicked.connect(
            lambda: transmitter.networkHandler.Transmission(self,transmitter)
        )

    def ConsoleAppendText(self,text,type):
        print(text + "\n")
        if type == 0:
            self.console_lock.acquire()
            self.CONSOLE.append(text + "\n")
            self.CONSOLE.update()
            self.console_lock.release()
            time.sleep(0.05)
