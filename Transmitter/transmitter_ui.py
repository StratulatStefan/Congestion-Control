# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'transmitter_ui.ui'
##
## Created by: Qt User Interface Compiler version 5.14.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(793, 855)
        MainWindow.setInputMethodHints(Qt.ImhLatinOnly)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.TITLE = QLabel(self.centralwidget)
        self.TITLE.setObjectName(u"TITLE")
        self.TITLE.setGeometry(QRect(90, 20, 621, 31))
        font = QFont()
        font.setFamily(u"Segoe UI Black")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75);
        self.TITLE.setFont(font)
        self.TITLE_2 = QLabel(self.centralwidget)
        self.TITLE_2.setObjectName(u"TITLE_2")
        self.TITLE_2.setGeometry(QRect(310, 60, 621, 31))
        self.TITLE_2.setFont(font)
        self.IP_LABEL = QLabel(self.centralwidget)
        self.IP_LABEL.setObjectName(u"IP_LABEL")
        self.IP_LABEL.setGeometry(QRect(100, 150, 71, 31))
        self.IP_LABEL.setFont(font)
        self.PORT_LABEL = QLabel(self.centralwidget)
        self.PORT_LABEL.setObjectName(u"PORT_LABEL")
        self.PORT_LABEL.setGeometry(QRect(410, 110, 121, 31))
        self.PORT_LABEL.setFont(font)
        self.IP = QTextEdit(self.centralwidget)
        self.IP.setObjectName(u"IP")
        self.IP.setGeometry(QRect(150, 150, 121, 31))
        font1 = QFont()
        font1.setFamily(u"Segoe UI Black")
        font1.setPointSize(9)
        font1.setBold(True)
        font1.setWeight(75);
        self.IP.setFont(font1)
        self.IP.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.IP.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.PORT_RX = QTextEdit(self.centralwidget)
        self.PORT_RX.setObjectName(u"PORT_RX")
        self.PORT_RX.setGeometry(QRect(550, 110, 121, 31))
        self.PORT_RX.setFont(font1)
        self.PORT_RX.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.PORT_RX.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.CREARESOCKET = QPushButton(self.centralwidget)
        self.CREARESOCKET.setObjectName(u"CREARESOCKET")
        self.CREARESOCKET.setGeometry(QRect(320, 260, 141, 31))
        font2 = QFont()
        font2.setFamily(u"Segoe UI")
        font2.setPointSize(10)
        font2.setBold(True)
        font2.setWeight(75);
        self.CREARESOCKET.setFont(font2)
        self.CREARESOCKETSTATUS = QLabel(self.centralwidget)
        self.CREARESOCKETSTATUS.setObjectName(u"CREARESOCKETSTATUS")
        self.CREARESOCKETSTATUS.setGeometry(QRect(280, 320, 271, 31))
        font3 = QFont()
        font3.setFamily(u"Segoe UI Black")
        font3.setPointSize(10)
        font3.setBold(True)
        font3.setWeight(75);
        self.CREARESOCKETSTATUS.setFont(font3)
        self.SELECTFILELABEL = QLabel(self.centralwidget)
        self.SELECTFILELABEL.setObjectName(u"SELECTFILELABEL")
        self.SELECTFILELABEL.setGeometry(QRect(100, 400, 171, 16))
        font4 = QFont()
        font4.setFamily(u"Segoe UI Black")
        font4.setPointSize(11)
        font4.setBold(True)
        font4.setWeight(75);
        self.SELECTFILELABEL.setFont(font4)
        self.SELECTFILE_TEXT = QTextEdit(self.centralwidget)
        self.SELECTFILE_TEXT.setObjectName(u"SELECTFILE_TEXT")
        self.SELECTFILE_TEXT.setEnabled(True)
        self.SELECTFILE_TEXT.setGeometry(QRect(280, 390, 271, 31))
        self.SELECTFILE_TEXT.setFont(font1)
        self.SELECTFILE_TEXT.setMouseTracking(False)
        self.SELECTFILE_TEXT.setAcceptDrops(False)
        self.SELECTFILE_TEXT.setInputMethodHints(Qt.ImhMultiLine)
        self.SELECTFILE_TEXT.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.SELECTFILE_TEXT.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.SELECTFILE_TEXT.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.BROWSE_FILE = QPushButton(self.centralwidget)
        self.BROWSE_FILE.setObjectName(u"BROWSE_FILE")
        self.BROWSE_FILE.setGeometry(QRect(570, 390, 101, 31))
        font5 = QFont()
        font5.setFamily(u"Segoe UI Black")
        font5.setBold(True)
        font5.setWeight(75);
        self.BROWSE_FILE.setFont(font5)
        self.IP_OK = QPushButton(self.centralwidget)
        self.IP_OK.setObjectName(u"IP_OK")
        self.IP_OK.setGeometry(QRect(290, 150, 51, 28))
        self.IP_OK.setFont(font1)
        self.PORT_OK_RX = QPushButton(self.centralwidget)
        self.PORT_OK_RX.setObjectName(u"PORT_OK_RX")
        self.PORT_OK_RX.setGeometry(QRect(690, 110, 41, 28))
        self.PORT_OK_RX.setFont(font1)
        self.START = QPushButton(self.centralwidget)
        self.START.setObjectName(u"START")
        self.START.setGeometry(QRect(290, 450, 171, 31))
        self.START.setFont(font1)
        self.CONSOLE = QTextEdit(self.centralwidget)
        self.CONSOLE.setObjectName(u"CONSOLE")
        self.CONSOLE.setGeometry(QRect(40, 500, 721, 291))
        font6 = QFont()
        font6.setFamily(u"Times New Roman")
        font6.setPointSize(9)
        font6.setBold(False)
        font6.setWeight(50);
        self.CONSOLE.setFont(font6)
        self.CONSOLE.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.CONSOLE.setToolTipDuration(-1)
        self.CONSOLE.setTabChangesFocus(True)
        self.PORT_TX = QTextEdit(self.centralwidget)
        self.PORT_TX.setObjectName(u"PORT_TX")
        self.PORT_TX.setGeometry(QRect(550, 180, 121, 31))
        self.PORT_TX.setFont(font1)
        self.PORT_TX.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.PORT_TX.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.PORT_OK_TX = QPushButton(self.centralwidget)
        self.PORT_OK_TX.setObjectName(u"PORT_OK_TX")
        self.PORT_OK_TX.setGeometry(QRect(690, 180, 41, 28))
        self.PORT_OK_TX.setFont(font1)
        self.PORT_LABEL_2 = QLabel(self.centralwidget)
        self.PORT_LABEL_2.setObjectName(u"PORT_LABEL_2")
        self.PORT_LABEL_2.setGeometry(QRect(410, 180, 131, 31))
        self.PORT_LABEL_2.setFont(font)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 793, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.TITLE.setText(QCoreApplication.translate("MainWindow", u"Transfer de fisiere. Mecanism de tratare a congestiei", None))
        self.TITLE_2.setText(QCoreApplication.translate("MainWindow", u"Transmisie", None))
        self.IP_LABEL.setText(QCoreApplication.translate("MainWindow", u"IP :  ", None))
        self.PORT_LABEL.setText(QCoreApplication.translate("MainWindow", u"PORT RX : ", None))
        self.IP.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Segoe UI Black'; font-size:9pt; font-weight:600; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'MS Shell Dlg 2'; font-size:7.8pt; font-weight:400;\"><br /></p></body></html>", None))
        self.CREARESOCKET.setText(QCoreApplication.translate("MainWindow", u"Creare Socket", None))
        self.CREARESOCKETSTATUS.setText("")
        self.SELECTFILELABEL.setText(QCoreApplication.translate("MainWindow", u"Selectati destinatia :", None))
        self.SELECTFILE_TEXT.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Segoe UI Black'; font-size:9pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">D:/Learning/RC/input/</span></p></body></html>", None))
        self.BROWSE_FILE.setText(QCoreApplication.translate("MainWindow", u"BROWSE", None))
        self.IP_OK.setText(QCoreApplication.translate("MainWindow", u"OK", None))
        self.PORT_OK_RX.setText(QCoreApplication.translate("MainWindow", u"OK", None))
        self.START.setText(QCoreApplication.translate("MainWindow", u"START TRANSMISIE", None))
        self.CONSOLE.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Times New Roman'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.PORT_OK_TX.setText(QCoreApplication.translate("MainWindow", u"OK", None))
        self.PORT_LABEL_2.setText(QCoreApplication.translate("MainWindow", u"PORT TX : ", None))
    # retranslateUi

