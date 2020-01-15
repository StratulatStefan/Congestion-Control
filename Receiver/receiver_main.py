import sys
from receiver_uinterface import *
from receiver_tahoe import *


class MainWindow(QMainWindow):
    def __init__(self,receiver):
        super(MainWindow, self).__init__()
        self.ui = Ui_Interface(self)
        self.ui.SetActions(receiver)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    receiver = ReceiverController()
    window = MainWindow(receiver)
    window.show()

    sys.exit(app.exec_())