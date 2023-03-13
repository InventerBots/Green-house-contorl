from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from threading import Thread
from collections import deque
import sys
import numpy
import os
import socket
import time
import tempCalc
import server

class ServerThread(QThread):
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
        self.tempRaw_12bit = []
        self.logset_rise = deque([])
        self.buff = 7200 # number of readings to keep, 7200 = 30s of data
        
    def run(self):
        self.server_obj = server.TCPServer()
    
    def mainLoop(self):
        if not self.is_connected:
            self.connect()
            
        if self.is_connected:
            self.server_obj.openConnection(self.conn_tup, 3)
            self.tempBuff.append(self.server_obj.tempRaw_12bit_int.copy())
        if len(self.tempBuff) > 2:
            self.tempBuff.popleft()
               
        '''
        Calculate temperature rise
        
        ''' 
        try:
            cTemp = self.tempBuff[0]
            pTemp = self.tempBuff[1]
            
            for c in range(len(cTemp)):
                cTemp_deg = numpy.array(tempCalc.convertRawToDeg_F(cTemp[c]))
            for p in range(len(pTemp)):
                pTemp_deg = numpy.array(tempCalc.convertRawToDeg_F(pTemp[p]))
            rise = numpy.subtract(pTemp_deg, cTemp_deg)
            
            self.logset_rise.append(rise)
            if len(self.logset_rise) > self.buff:
                self.logset_rise.popleft()
                
            print(len(self.logset_rise))
        except:
            pass
        
    def connect(self):
        if not self.conn_tup and not self.is_connected:
            self.conn_tup = self.server_obj.acceptConnection()
            print('Connected to {}'.format(self.conn_tup[1]))
            self.is_connected = True
        
    def disconnect(self):
        if not self.is_connected and self.conn_tup:
            self.server_obj.disconnect(self.conn_tup)
            self.is_connected = False
            
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.initUI()
        
        self.timer = QTimer()
        self.timer.setInterval(250)
        self.timer.timeout.connect(self.runServer)
        
        self.display_val = []
        self.display_ind = 0
        self.buff = 0
        self.server_thread = None
        
    def initUI(self):
        self.valMinWidth = 160
        self.setWindowTitle("Greenhouse Control panel")
        self.setStyleSheet("background-color : rgb(47, 62, 67)")
        # self.setMinimumSize(800, 480)
        
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

        self.b_Connect = QPushButton("Start server")
        self.b_Connect.setFont(QFont('Default', 15))
        self.b_Connect.setStyleSheet("background-color : rgb(21, 93, 197); color : white")
        self.b_Connect.setMinimumHeight(50)
        self.b_Connect.clicked.connect(self.startServer)
        
        self.b_Disconnect = QPushButton("Stop server")
        self.b_Disconnect.setFont(QFont('Default', 15))
        self.b_Disconnect.setStyleSheet("background-color : rgb(21, 93, 197); color : white")
        self.b_Disconnect.setMinimumHeight(50)
        self.b_Disconnect.clicked.connect(self.stopServer)
        
        self.pb_Dataset = QProgressBar(self)
        self.pb_Dataset.setRange(0, 7200)
        
        '''
        Layoyts
        
        '''
        mainLayout = QGridLayout()
        dataLayout_main = QHBoxLayout()
        dataLayout_col1 = QFormLayout()
        dataLayout_col2 = QFormLayout()
        dataBarLayout = QVBoxLayout()
        btnLayout = QHBoxLayout()
        fanLayout = QVBoxLayout()
        
        dataLayout_col1.addRow(self.val_1_label, self.l_Val_1)
        dataLayout_col1.addRow(self.val_3_label, self.l_Val_3)
        dataLayout_col1.addRow(self.val_5_label, self.l_Val_5)
        dataLayout_col2.addRow(self.val_2_label, self.l_Val_2)
        dataLayout_col2.addRow(self.val_4_label, self.l_Val_4)
        dataLayout_col2.addRow(self.val_6_label, self.l_Val_6)

        dataLayout_main.addLayout(dataLayout_col1)
        dataLayout_main.addLayout(dataLayout_col2)
        dataBarLayout.addWidget(self.pb_Dataset)
        btnLayout.addWidget(self.b_Connect)
        btnLayout.addWidget(self.b_Disconnect)
        
        mainLayout.addLayout(dataLayout_main, 0, 0)
        mainLayout.addLayout(dataBarLayout, 1, 0)
        mainLayout.addLayout(btnLayout, 2, 0)
        mainLayout.addLayout(fanLayout, 0, 2, 1, 2)

        lay = QWidget()
        lay.setLayout(mainLayout)

        self.setCentralWidget(lay)
        self.show()

        self.timer = QTimer()
        self.timer.setInterval(250)
        self.timer.timeout.connect(self.runServer)
        self.timer.start()

    def startServer(self):
        if not self.server_thread:
            print('starting server thread')
            self.server_thread = ServerThread()
            self.server_thread.start()
            self.timer.start()
            self.buff = self.server_thread.buff
            
            self.l_Val_1.setStyleSheet("color : rgb(255, 255, 255)")
            self.l_Val_2.setStyleSheet("color : rgb(255, 255, 255)")
            self.l_Val_3.setStyleSheet("color : rgb(255, 255, 255)")
            # self.l_Val_4.setStyleSheet("color : rgb(0, 0, 0)")
            # self.l_Val_5.setStyleSheet("color : rgb(0, 0, 0)")
            # self.l_Val_6.setStyleSheet("color : rgb(0, 0, 0)")
        
    def runServer(self):
        if not self.server_thread:
            return -1
        self.server_thread.mainLoop()
        
        self.pb_Dataset.setValue(len(self.server_thread.logset_rise))
        if self.display_ind < 4:
            self.display_val.append(self.server_thread.tempBuff[0])
            self.display_ind += 1
        else:
            self.l_Val_1.setText(str('%.2f' % tempCalc.convertRawToDeg_F(numpy.average(self.display_val[0]))) + ' °F')
            self.l_Val_2.setText(str('%.2f' % tempCalc.convertRawToDeg_F(numpy.average(self.display_val[1]))) + ' °F')
            self.l_Val_3.setText(str('%.2f' % tempCalc.convertRawToDeg_F(numpy.average(self.display_val[2]))) + ' °F')
            
            self.display_ind = 0
            self.display_val.clear()
        
    def stopServer(self):
        if self.server_thread:
            self.timer.stop()
            self.server_thread.disconnect()
            self.server_thread.quit()
            self.server_thread = None
            if self.server_thread == None:
                print('thread closed')
        
        self.l_Val_1.setStyleSheet("color : rgb(68, 81, 86)")
        self.l_Val_2.setStyleSheet("color : rgb(68, 81, 86)")
        self.l_Val_3.setStyleSheet("color : rgb(68, 81, 86)")
        self.l_Val_4.setStyleSheet("color : rgb(68, 81, 86)")
        self.l_Val_5.setStyleSheet("color : rgb(68, 81, 86)")
        self.l_Val_6.setStyleSheet("color : rgb(68, 81, 86)")
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
