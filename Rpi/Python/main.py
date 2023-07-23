from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from collections import deque
import sys
import numpy
import tempCalc
import server
import mariadb as db
from datetime import datetime
import netifaces as ni

MAX_SENSORS = 5
SENSORS_CONNECTED = 4

class DatabaseInterface():
    def __init__(self):
        super().__init__()
        try:
            self.dbConn = db.connect(
                user="gh",
                password="admin",
                host="127.0.0.1",
                port=3306,
                database="ghdb"
            )
        except db.Error as e:
            print(f"Error connecting to MariaDB Paltform: {e}")
            sys.exit(1)
        self.dbCursor = self.dbConn.cursor()

        self.date_MDY = datetime.today().strftime("%m_%d_%Y")
        self.time_HMS = datetime.today().strftime("%H_%M")

    def createTable(self):
        # self.tableName = f"dataset_{self.date_MDY}"
        self.tableName = "dataset"
        try:
            self.dbCursor.execute(f"""CREATE TABLE {self.tableName} 
            (id INT AUTO_INCREMENT PRIMARY KEY, Date_Time CHAR(128), Output_0 int, Output_1 int, Input_0 int, Input_1 int, Input_2 int, Input_3 int);""")
            print("table created")
        except db.Error as e:
            if "already exists" not in str(e):
                print(e)
        return self.tableName

    def insertIntoTable(self, table, Output_0 = int, Output_1 = int, Input_0 = int, Input_1 = int, Input_2 = int, Input_3 = int):
        try:
            self.dbCursor.execute(f"""INSERT INTO {self.tableName} (Date_Time, Output_0, Output_1, Input_0, Input_1, Input_2, Input_3) VALUES 
                (NOW(), {Output_0}, {Output_1}, {Input_0}, {Input_1}, {Input_2}, {Input_3})""")
            self.dbConn.commit()
            
        except db.Error as e:
            print(e)

    def closeConnection(self):
        self.dbCursor.close()
        self.dbConn.close()


class ServerThread(QThread):
    signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        
        self.is_connected = False
        self.conn_tup = None
        self.tempBuff = deque([])
        self.tempRaw_12bit = []
        self.logset_rise = deque([])
        self.buff = 7200 # number of readings to keep, 7200 = 30m of data

        self.connectedIP = ''
        
    def run(self):
        self.server_obj = server.TCPServer()
    
    def mainLoop(self):
        if not self.is_connected:
            self.connect()
            
        if self.is_connected:
            self.server_obj.openConnection(self.conn_tup, SENSORS_CONNECTED)
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
            try:
                ConnectionsWindow.remote_ip = str('{}'.format(self.conn_tup[1][0]))
            except:
                pass
            self.is_connected = True
        
    def disconnect(self):
        if not self.is_connected and self.conn_tup:
            self.server_obj.disconnect(self.conn_tup)
            self.is_connected = False
            
class ConnectionsWindow(QWidget):
    remote_ip = 'N/A'
    def __init__(self):
        super().__init__()
        self.setWindowTitle("List of connections")
        self.setMinimumWidth(300)
        self.layout = QVBoxLayout()
        self.connection_l_1 = QLabel()
        
        self.ip = ni.ifaddresses('enp0s3')[ni.AF_INET][0]['addr']
        
        if self.remote_ip != 'N/A':
            self.connection_l_1.setText(self.ip+' <- '+self.remote_ip)
            self.connection_l_1.setStyleSheet("color : rgb(0, 255, 0)")

        self.layout.addWidget(self.connection_l_1)
        self.setLayout(self.layout)

class MainWindow(QMainWindow):
    POLL_TIMER = 250
    LOG_INTERVAL = 300 # log interval in seconds
    server_thread = None

    def __init__(self):
        super().__init__()
        self.initUI()

        self.dbInterface = DatabaseInterface()
        self.dbInterface.createTable()
        
        self.timer = QTimer()
        self.timer.setInterval(250)
        self.timer.timeout.connect(self.runServer)
        
        self.display_val = []
        self.display_ind = 0
        self.log_ind = -1
        self.buff = 0

        
        
    def initUI(self):
        self.valMinWidth = 160
        self.setWindowTitle("Greenhouse Control panel")
        self.setStyleSheet("background-color : rgb(31, 31, 31)")
        self.setMinimumSize(1024, 600)

        self.toolbar = QToolBar("toolbar")
        self.toolbar.setStyleSheet("background-color : rgb(37 ,90 ,144)")
        self.addToolBar(self.toolbar)

        self.menu_bar = self.menuBar()
        
        self.file_menu = self.menu_bar.addMenu("&File")
        self.edit_menu = self.menu_bar.addMenu("&Edit")
        self.connection_menu = self.menu_bar.addMenu("&Connections")

        self.menu_b_fullscreen = QAction("Fullscreen")
        self.menu_b_fullscreen.triggered.connect(self.showFullScreen)
        self.file_menu.addAction(self.menu_b_fullscreen)

        self.menu_b_connect = QAction("Connect client", self)
        self.menu_b_connect.triggered.connect(self.startServer)
        self.connection_menu.addAction(self.menu_b_connect)

        self.menu_b_disconnect = QAction("disconnect client", self)
        self.menu_b_disconnect.triggered.connect(self.stopServer)
        self.connection_menu.addAction(self.menu_b_disconnect)

        self.menu_c_toolbar_button = QAction("Show toolbar buttons")
        self.menu_c_toolbar_button.setCheckable(True)
        self.menu_c_toolbar_button.triggered.connect(self.showConnectionToolbar)
        self.connection_menu.addAction(self.menu_c_toolbar_button)

        self.toolbar_b_connect = QAction("Connect client", self)
        self.toolbar_b_connect.setToolTip("Connect to remote device")
        self.toolbar_b_connect.triggered.connect(self.startServer)
        self.toolbar_b_connect.setVisible(False)
        self.toolbar.addAction(self.toolbar_b_connect)

        self.toolbar_b_deviceIP = QAction("Active connections", self)
        self.toolbar_b_deviceIP.setToolTip("List all active connections")
        self.toolbar_b_deviceIP.triggered.connect(self.openConnectionsWindow)
        self.toolbar.addAction(self.toolbar_b_deviceIP)

        self.toolbar.addSeparator()

        self.toolbar_l_localIP = QLabel(ni.ifaddresses('enp0s3')[ni.AF_INET][0]['addr'])
        self.toolbar_l_localIP.setToolTip("Local device IP")
        self.toolbar.addWidget(self.toolbar_l_localIP)

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
        # mainLayout.addLayout(btnLayout, 2, 0)
        mainLayout.addLayout(fanLayout, 0, 2, 1, 2)

        lay = QWidget()
        lay.setLayout(mainLayout)

        self.setCentralWidget(lay)
        self.show()

        self.timer = QTimer()
        self.timer.setInterval(int(self.POLL_TIMER))
        self.timer.timeout.connect(self.runServer)
        self.timer.start()

    def showConnectionToolbar(self):
        print(self.menu_c_toolbar_button.isChecked())
        if self.menu_c_toolbar_button.isChecked:
            self.toolbar_b_connect.setVisible(True)
        else:
            self.toolbar_b_connect.setVisible(False)

    def openConnectionsWindow(self):
        self.connections = ConnectionsWindow()
        self.connections.show()

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
            self.l_Val_4.setStyleSheet("color : rgb(255, 255, 255)")
            # self.l_Val_4.setStyleSheet("color : rgb(0, 0, 0)")
            # self.l_Val_5.setStyleSheet("color : rgb(0, 0, 0)")
            # self.l_Val_6.setStyleSheet("color : rgb(0, 0, 0)")
        
    def runServer(self):
        tempList = []
        valToDisplay = []

        if not self.server_thread:
            return -1
        self.server_thread.mainLoop()
        
        self.pb_Dataset.setValue(len(self.server_thread.logset_rise))
        if self.display_ind < 4:
            self.display_val.append(self.server_thread.tempBuff[0])
            self.display_ind += 1
        else:
            for lab in range(MAX_SENSORS):
                try:
                    for x in range(len(self.display_val)):
                        tempList.append(self.display_val[x][lab])
                except:
                    pass
                valToDisplay.append(tempList.copy())
                tempList.clear()
            self.l_Val_1_dis = tempCalc.convertRawToDeg_F(numpy.average(valToDisplay[0]))
            self.l_Val_2_dis = tempCalc.convertRawToDeg_F(numpy.average(valToDisplay[1]))
            self.l_Val_3_dis = tempCalc.convertRawToDeg_F(numpy.average(valToDisplay[2]))
            self.l_Val_4_dis = tempCalc.convertRawToDeg_F(numpy.average(valToDisplay[3]))

            self.l_Val_1.setText(str('%.2f' % self.l_Val_1_dis) + ' °F')
            self.l_Val_2.setText(str('%.2f' % self.l_Val_2_dis) + ' °F')
            self.l_Val_3.setText(str('%.2f' % self.l_Val_3_dis) + ' °F')
            self.l_Val_4.setText(str('%.2f' % self.l_Val_4_dis) + ' °F')
            
            if self.log_ind == -1: # log first reading at startup
                self.logData(0, 0, self.l_Val_1_dis, self.l_Val_2_dis, self.l_Val_3_dis, self.l_Val_4_dis)
            self.log_ind += 1

            self.display_ind = 0
            self.display_val.clear()

        
        if self.log_ind >= self.LOG_INTERVAL: 
            self.logData(0, 0, self.l_Val_1_dis, self.l_Val_2_dis, self.l_Val_3_dis, self.l_Val_4_dis)
            self.log_ind = 0

    def logData(self,Output0=int, Output1=int, Input0=int, Input1=int, Input2=int, Input3=int):
        table = self.dbInterface.createTable()
        print("logged data")
        self.dbInterface.insertIntoTable(table, Output0, Output1, Input0, Input1, Input2, Input3)

    def stopServer(self):
        if self.server_thread:
            self.timer.stop()
            self.server_thread.disconnect()
            self.server_thread.quit()
            self.server_thread = None
            ConnectionsWindow.remote_ip = 'N/A'
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
