import sys
from transmitter_uinterface import *
from transmitter_tahoe import *


class MainWindow(QMainWindow):
    def __init__(self,transmitter):
        super(MainWindow, self).__init__()
        self.ui = Ui_Interface(self)
        self.ui.SetActions(transmitter)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    transmitter = TransmitterController()
    window = MainWindow(transmitter)
    window.show()

    sys.exit(app.exec_())
