from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from threading import Thread
from collections import deque
import sys
import socket
import time
import tempCalc
import server

class WorkerThread(QThread):
    signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.setInterval(250)
        self.timer.timeout.connect(self.mainLoop)
        # self.timer.start()
        
        self.is_connected = False
        self.conn_tup = None
        self.tempBuff = deque([])
        
    def run(self):
        self.server_obj = server.TCPServer()
    
    def mainLoop(self):
        self.connect()
        # print(self.conn_tup)
        
        # if self.conn_tup and not self.is_connected:
        #     self.server_obj.disconnect()
            
        if len(self.tempBuff) < 1: # no connection has been established 
            return
        if self.is_connected:
            self.tempBuff.append(self.server_obj.openConnection(self.conn_tup, 3))
        if len(self.tempBuff) > 2:
            self.tempBuff.popleft()
        # print(self.tempBuff)
        print(self.is_connected)
        
    def connect(self):
        if not self.conn_tup and self.is_connected:
            self.conn_tup = self.server_obj.acceptConnection()
            print('Connected to {}'.format(self.conn_tup[1]))
        
    def disconnect(self):
        if not self.is_connected and self.conn_tup:
            self.server_obj.disconnect(self.conn_tup)
            
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.initUI()
        
        # Setup server thread
        self.server_thread = None
        # self.server_thread = WorkerThread()
        # self.server_thread.start()
        
        self.server_running = False
        
        local_IP = socket.gethostbyname(socket.gethostname())

    def initUI(self):
        self.valMinWidth = 160
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
        self.l_Val_1.setMinimumWidth(self.valMinWidth)
        self.l_Val_1.setAlignment(Qt.AlignmentFlag.AlignLeading)
        self.l_Val_1.setMargin(5)

        self.val_2_label = QLabel("2")
        self.val_2_label.setFont(QFont('Default', 20))
        self.val_2_label.setStyleSheet("color : rgb(128, 128, 128)")
        self.val_2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.l_Val_2 = QLabel("N/A")
        self.l_Val_2.setFont(QFont('Default', 30))
        self.l_Val_2.setStyleSheet("color : rgb(68, 81, 86)")
        self.l_Val_2.setMinimumWidth(self.valMinWidth)
        self.l_Val_2.setAlignment(Qt.AlignmentFlag.AlignLeading)
        self.l_Val_2.setMargin(5)

        self.val_3_label = QLabel("3")
        self.val_3_label.setFont(QFont('Default', 20))
        self.val_3_label.setStyleSheet("color : rgb(128, 128, 128)")
        self.val_3_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.l_Val_3 = QLabel("N/A")
        self.l_Val_3.setFont(QFont('Default', 30))
        self.l_Val_3.setStyleSheet("color : rgb(68, 81, 86)")
        self.l_Val_3.setMinimumWidth(self.valMinWidth)
        self.l_Val_3.setAlignment(Qt.AlignmentFlag.AlignLeading)
        self.l_Val_3.setMargin(5)

        self.val_4_label = QLabel("4")
        self.val_4_label.setFont(QFont('Default', 20))
        self.val_4_label.setStyleSheet("color : rgb(128, 128, 128)")
        self.val_4_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.l_Val_4 = QLabel("N/A")
        self.l_Val_4.setFont(QFont('Default', 30))
        self.l_Val_4.setStyleSheet("color : rgb(68, 81, 86)")
        self.l_Val_4.setMinimumWidth(self.valMinWidth)
        self.l_Val_4.setAlignment(Qt.AlignmentFlag.AlignLeading)
        self.l_Val_4.setMargin(5)

        self.val_5_label = QLabel("5")
        self.val_5_label.setFont(QFont('Default', 20))
        self.val_5_label.setStyleSheet("color : rgb(128, 128, 128)")
        self.val_5_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.l_Val_5 = QLabel("N/A")
        self.l_Val_5.setFont(QFont('Default', 30))
        self.l_Val_5.setStyleSheet("color : rgb(68, 81, 86)")
        self.l_Val_5.setMinimumWidth(self.valMinWidth)
        self.l_Val_5.setAlignment(Qt.AlignmentFlag.AlignLeading)
        self.l_Val_5.setMargin(5)

        self.val_6_label = QLabel("6")
        self.val_6_label.setFont(QFont('Default', 20))
        self.val_6_label.setStyleSheet("color : rgb(128, 128, 128)")
        self.val_6_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.l_Val_6 = QLabel("N/A")
        self.l_Val_6.setFont(QFont('Default', 30))
        self.l_Val_6.setStyleSheet("color : rgb(68, 81, 86)")
        self.l_Val_6.setMinimumWidth(self.valMinWidth)
        self.l_Val_6.setAlignment(Qt.AlignmentFlag.AlignLeading)
        self.l_Val_6.setMargin(5)

        self.l_rise_1 = QLabel('N/A')
        self.l_rise_1.setFont(QFont('Default', 25))
        self.l_rise_1.setStyleSheet("color : rgb(68, 81, 86)")

        b_Connect = QPushButton("Connect Client")
        b_Connect.setFont(QFont('Default', 15))
        b_Connect.setStyleSheet("background-color : rgb(21, 93, 197); color : white")
        b_Connect.setMinimumHeight(50)
        b_Connect.clicked.connect(self.connectClient)
        
        b_Disconnect = QPushButton("Disconnect Client")
        b_Disconnect.setFont(QFont('Default', 15))
        b_Disconnect.setStyleSheet("background-color : rgb(21, 93, 197); color : white")
        b_Disconnect.setMinimumHeight(50)
        b_Disconnect.clicked.connect(self.disconnectClient)

        dataLayout_col1.addRow(self.val_1_label, self.l_Val_1)
        dataLayout_col1.addRow(self.val_3_label, self.l_Val_3)
        dataLayout_col1.addRow(self.val_5_label, self.l_Val_5)
        dataLayout_col2.addRow(self.val_2_label, self.l_Val_2)
        dataLayout_col2.addRow(self.val_4_label, self.l_Val_4)
        dataLayout_col2.addRow(self.val_6_label, self.l_Val_6)

        dataLayout_main.addLayout(dataLayout_col1)
        dataLayout_main.addLayout(dataLayout_col2)
        btnLayout.addWidget(b_Connect)
        btnLayout.addWidget(b_Disconnect)

        mainLayout.addLayout(dataLayout_main, 0, 0)
        mainLayout.addLayout(btnLayout, 1, 0)
        mainLayout.addLayout(fanLayout, 0, 2, 1, 2)

        lay = QWidget()
        lay.setLayout(mainLayout)

        self.setCentralWidget(lay)
        self.show()

        # self.timer = QTimer()
        # self.timer.setInterval(250)
        # self.timer.timeout.connect(self.runServer)
        # self.timer.start()

    def connectClient(self):
        print("connecting")
        if not self.server_thread:
            print('starting server thread')
            self.server_thread = WorkerThread()
            self.server_thread.start()
        # self.server_thread.connect()
        self.server_thread.timer.start()
        self.server_thread.is_connected = True
   
    def disconnectClient(self):
        print("disconnecting")
        self.server_thread.timer.stop()
        self.server_thread.is_connected = False
        self.server_thread.disconnect()
        self.server_thread.quit()
        self.server_thread = None
        if self.server_thread == None:
            print('thread closed')
        
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
