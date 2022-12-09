from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import server

import time
class MainWindow(QMainWindow):
    connectionStat = False
    displayRefreshRate = 5 # refresh display every 5 seconds
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.counter = 0
        valMinWidth = 150

        self.setWindowIcon(QIcon('pyLogo.png'))
        self.setWindowTitle("Greenhouse Control panel: Disconnected")
        self.setStyleSheet("background-color : rgb(47, 62, 67)")
        # self.setMinimumSize(800, 480)
        
        mainLayout = QGridLayout()
        dataLayout_main = QHBoxLayout()
        dataLayout_col1 = QFormLayout()
        dataLayout_col2 = QFormLayout()
        btnLayout = QHBoxLayout()
        fanLayout = QVBoxLayout()

        self.val_1_label = QLabel("1")
        self.val_1_label.setFont(QFont('Default', 20))
        self.val_1_label.setStyleSheet("color : rgb(128, 128, 128)")
        self.val_1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.l_Val_1 = QLabel("N/A")
        self.l_Val_1.setFont(QFont('Default', 30))
        self.l_Val_1.setStyleSheet("color : rgb(68, 81, 86)")
        self.l_Val_1.setMinimumWidth(valMinWidth)
        self.l_Val_1.setAlignment(Qt.AlignmentFlag.AlignLeading)
        self.l_Val_1.setMargin(5)

        self.val_2_label = QLabel("2")
        self.val_2_label.setFont(QFont('Default', 20))
        self.val_2_label.setStyleSheet("color : rgb(128, 128, 128)")
        self.val_2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.l_Val_2 = QLabel("N/A")
        self.l_Val_2.setFont(QFont('Default', 30))
        self.l_Val_2.setStyleSheet("color : rgb(68, 81, 86)")
        self.l_Val_2.setMinimumWidth(valMinWidth)
        self.l_Val_2.setAlignment(Qt.AlignmentFlag.AlignLeading)
        self.l_Val_2.setMargin(5)

        self.val_3_label = QLabel("3")
        self.val_3_label.setFont(QFont('Default', 20))
        self.val_3_label.setStyleSheet("color : rgb(128, 128, 128)")
        self.val_3_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.l_Val_3 = QLabel("N/A")
        self.l_Val_3.setFont(QFont('Default', 30))
        self.l_Val_3.setStyleSheet("color : rgb(68, 81, 86)")
        self.l_Val_3.setMinimumWidth(valMinWidth)
        self.l_Val_3.setAlignment(Qt.AlignmentFlag.AlignLeading)
        self.l_Val_3.setMargin(5)

        self.val_4_label = QLabel("4")
        self.val_4_label.setFont(QFont('Default', 20))
        self.val_4_label.setStyleSheet("color : rgb(128, 128, 128)")
        self.val_4_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.l_Val_4 = QLabel("N/A")
        self.l_Val_4.setFont(QFont('Default', 30))
        self.l_Val_4.setStyleSheet("color : rgb(68, 81, 86)")
        self.l_Val_4.setMinimumWidth(valMinWidth)
        self.l_Val_4.setAlignment(Qt.AlignmentFlag.AlignLeading)
        self.l_Val_4.setMargin(5)

        self.val_5_label = QLabel("5")
        self.val_5_label.setFont(QFont('Default', 20))
        self.val_5_label.setStyleSheet("color : rgb(128, 128, 128)")
        self.val_5_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.l_Val_5 = QLabel("N/A")
        self.l_Val_5.setFont(QFont('Default', 30))
        self.l_Val_5.setStyleSheet("color : rgb(68, 81, 86)")
        self.l_Val_5.setMinimumWidth(valMinWidth)
        self.l_Val_5.setAlignment(Qt.AlignmentFlag.AlignLeading)
        self.l_Val_5.setMargin(5)

        self.val_6_label = QLabel("6")
        self.val_6_label.setFont(QFont('Default', 20))
        self.val_6_label.setStyleSheet("color : rgb(128, 128, 128)")
        self.val_6_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.l_Val_6 = QLabel("N/A")
        self.l_Val_6.setFont(QFont('Default', 30))
        self.l_Val_6.setStyleSheet("color : rgb(68, 81, 86)")
        self.l_Val_6.setMinimumWidth(valMinWidth)
        self.l_Val_6.setAlignment(Qt.AlignmentFlag.AlignLeading)
        self.l_Val_6.setMargin(5)

        self.connectedIP = QLabel() 
        self.connectedIP.setFont(QFont('Default', 10))
        self.connectedIP.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.connectedIP.hide()

        b_Connect = QPushButton("Connect Client")
        b_Connect.setFont(QFont('Default', 15))
        b_Connect.setStyleSheet("background-color : rgb(21, 93, 197); color : white")
        b_Connect.setMinimumHeight(50)
        b_Connect.pressed.connect(self.connectClient)
        
        b_Disconnect = QPushButton("Disconnect Client")
        b_Disconnect.setFont(QFont('Default', 15))
        b_Disconnect.setStyleSheet("background-color : rgb(21, 93, 197); color : white")
        b_Disconnect.setMinimumHeight(50)
        b_Disconnect.pressed.connect(self.disconnectClient)

        dataLayout_col1.addRow(self.val_1_label, self.l_Val_1)
        dataLayout_col1.addRow(self.val_3_label, self.l_Val_3)
        dataLayout_col1.addRow(self.val_5_label, self.l_Val_5)
        dataLayout_col2.addRow(self.val_2_label, self.l_Val_2)
        dataLayout_col2.addRow(self.val_4_label, self.l_Val_4)
        dataLayout_col2.addRow(self.val_6_label, self.l_Val_6)

        dataLayout_main.addLayout(dataLayout_col1)
        dataLayout_main.addLayout(dataLayout_col2)
        btnLayout.addWidget(b_Connect)
        btnLayout.addWidget(self.connectedIP)
        btnLayout.addWidget(b_Disconnect)

        mainLayout.addLayout(dataLayout_main, 0, 0)
        mainLayout.addLayout(btnLayout, 1, 0)
        mainLayout.addLayout(fanLayout, 0, 2, 1, 2)

        lay = QWidget()
        lay.setLayout(mainLayout)

        self.setCentralWidget(lay)
        self.show()

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()

    def connectClient(self):
        print("connecting")
        # self.connectedIP.show()
        ip = server.Server.connect(server)
        self.connectionStat = True
        print("connected")
        self.setWindowTitle("Greenhouse Control panel: "+str(ip))
        self.l_Val_1.setStyleSheet("color : rgb(255, 255, 255)")
        self.l_Val_2.setStyleSheet("color : rgb(255, 255, 255)")
        self.l_Val_3.setStyleSheet("color : rgb(255, 255, 255)")
        # self.l_Val_4.setStyleSheet("color : rgb(0, 0, 0)")
        # self.l_Val_5.setStyleSheet("color : rgb(0, 0, 0)")
        # self.l_Val_6.setStyleSheet("color : rgb(0, 0, 0)")
    
    def disconnectClient(self):
        server.Server.disconnect(server)
        self.connectionStat = False
        self.counter = 0
        print("disconnected")
        self.setWindowTitle("Greenhouse Control panel: Disconnected")
        self.l_Val_1.setStyleSheet("color : rgb(68, 81, 86)")
        self.l_Val_2.setStyleSheet("color : rgb(68, 81, 86)")
        self.l_Val_3.setStyleSheet("color : rgb(68, 81, 86)")
        self.l_Val_4.setStyleSheet("color : rgb(68, 81, 86)")
        self.l_Val_5.setStyleSheet("color : rgb(68, 81, 86)")
        self.l_Val_6.setStyleSheet("color : rgb(68, 81, 86)")
        self.connectedIP.clear()
        self.connectedIP.hide()

    def recurring_timer(self):
        if self.connectionStat == False:
            return

        server.Server.read_rawTemp(server, 3)
        if self.displayRefreshRate <= 5:
            self.displayRefreshRate += 1
            return
        self.l_Val_1.setText(str('%.2f' % server.Server.convertRawToDeg_F(server.tempRaw_12bit_int[0]))+" °F")
        self.l_Val_2.setText(str('%.2f' % server.Server.convertRawToDeg_F(server.tempRaw_12bit_int[1]))+" °F")
        self.l_Val_3.setText(str('%.2f' % server.Server.convertRawToDeg_F(server.tempRaw_12bit_int[2]))+" °F")
        server.tempRaw_12bit_int.clear()
        self.displayRefreshRate = 0
        
        # self.counter +=1
        # self.l_Val_1.setText(str(self.counter))

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    app.exec()