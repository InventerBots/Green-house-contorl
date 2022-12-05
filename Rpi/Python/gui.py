from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import server

import time
class MainWindow(QMainWindow):
    connectionStat = False
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.counter = 0
        valMinWidth = 150

        self.setWindowTitle("Greenhouse Control panel: Disconnected")
        self.setStyleSheet("background-color : black")\
        
        layout = QGridLayout()

        self.l_Val_1 = QLabel("N/A")
        self.l_Val_1.setFont(QFont('Default', 30))
        self.l_Val_1.setStyleSheet("background-color : white")
        self.l_Val_1.setMinimumWidth(valMinWidth)
        self.l_Val_1.setAlignment(Qt.AlignCenter)
        self.l_Val_1.setMargin(5)

        self.l_Val_2 = QLabel("N/A")
        self.l_Val_2.setFont(QFont('Default', 30))
        self.l_Val_2.setStyleSheet("background-color : white")
        self.l_Val_2.setMinimumWidth(valMinWidth)
        self.l_Val_2.setAlignment(Qt.AlignCenter)
        self.l_Val_2.setMargin(5)
        
        self.l_Val_3 = QLabel("N/A")
        self.l_Val_3.setFont(QFont('Default', 30))
        self.l_Val_3.setStyleSheet("background-color : white")
        self.l_Val_3.setMinimumWidth(valMinWidth)
        self.l_Val_3.setAlignment(Qt.AlignCenter)
        self.l_Val_3.setMargin(5)

        b_Connect = QPushButton("Connect Client")
        b_Connect.setStyleSheet("background-color : gray")
        b_Connect.setFont(QFont('Default', 15))
        b_Connect.pressed.connect(self.connectClient)
        
        b_Disconnect = QPushButton("Disconnect Client")
        b_Disconnect.setStyleSheet("background-color : gray")
        b_Disconnect.setFont(QFont('Default', 15))
        b_Disconnect.pressed.connect(self.disconnectClient)

        layout.addWidget(self.l_Val_1, 0, 0)
        layout.addWidget(self.l_Val_2, 0, 1)
        layout.addWidget(self.l_Val_3, 0, 3)
        layout.addWidget(b_Connect, 1, 0)
        layout.addWidget(b_Disconnect, 1, 3)

        lay = QWidget()
        lay.setLayout(layout)

        self.setCentralWidget(lay)
        self.show()

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()

    def connectClient(self):
        print("connecting")
        server.Server.connect(server)
        self.connectionStat = True
        print("connected")
        self.setWindowTitle("Greenhouse Control panel: Connected")

    
    def disconnectClient(self):
        server.Server.disconnect(server)
        self.connectionStat = False
        self.counter = 0
        print("disconnected")
        self.setWindowTitle("Greenhouse Control panel: Disconnected")


    def recurring_timer(self):
        if self.connectionStat == False:
            return

        server.Server.read_rawTemp(server, 3)
        self.l_Val_1.setText(str(server.tempRaw_12bit_int[0]))
        self.l_Val_2.setText(str(server.tempRaw_12bit_int[1]))
        self.l_Val_3.setText(str(server.tempRaw_12bit_int[2]))
        server.tempRaw_12bit_int.clear()
        # self.counter +=1
        # self.l_Val_1.setText(str(self.counter))

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    app.exec_()