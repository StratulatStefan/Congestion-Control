import time
from threading import RLock
from  receiver_ui import *

class Ui_Interface(Ui_MainWindow):
    def __init__(self,window):
        self.console_lock = RLock()
        self.setupUi(window)

    def SetActions(self,receiver):
        self.IP_OK.clicked.connect(
            lambda : receiver.networkHandler.setIp(self,receiver,self.IP.toPlainText())
        )
        self.PORT_OK_RX.clicked.connect(
            lambda : receiver.networkHandler.setPortRX(self,receiver,self.PORT_RX.toPlainText())
        )
        self.PORT_OK_TX.clicked.connect(
            lambda : receiver.networkHandler.setPortTX(self,receiver,self.PORT_TX.toPlainText())
        )
        self.PORT_OK_PPP.clicked.connect(
            lambda : receiver.networkHandler.setLossProbability(self,receiver,self.LABEL_PPP.toPlainText())
        )
        self.CREARESOCKET.clicked.connect(
            lambda : self.CREARESOCKETSTATUS.setText(receiver.networkHandler.creareSocket(self,receiver))
        )
        self.BROWSE_FILE.clicked.connect(
            lambda: receiver.networkHandler.BrowseFile(self,receiver)
        )
        self.START.clicked.connect(
            lambda: receiver.networkHandler.Reception(self,receiver)
        )

    def ConsoleAppendText(self,text):
        self.console_lock.acquire()
        self.CONSOLE.append(text + "\n")
        self.CONSOLE.update()
        self.console_lock.release()
        time.sleep(0.05)
