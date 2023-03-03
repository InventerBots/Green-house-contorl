import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from time import sleep, process_time
import server_old as server_old
class window(QWidget):
    DisplayWidth = 800
    DisplayHeight = 480
    sensVal = 0
    connectionStat = False
    
    def __init__(self):
        super(window, self).__init__()
        self.resize(self.DisplayWidth, self.DisplayHeight)
        self.setStyleSheet("background-color : black")
        self.move(0,0)
        self.setWindowTitle("Greenhouse control panel")
        self.initUI()

    def initUI(self):
        self.fConnection = QFrame(self)
        self.fConnection.resize(250, 126)
        self.fConnection.setFrameShape(QFrame.StyledPanel)
        self.fConnection.setLineWidth(1)
        self.fConnection.setStyleSheet("background-color : white")
        self.fConnection.move(25, 25)

        self.fConnInd = QFrame(self)
        self.fConnInd.resize(10, 10)
        self.fConnInd.setStyleSheet("background-color : red")
        self.fConnInd.move(252, 38)
        
        self.lConnStat = QLabel(self)
        self.lConnStat.setText("No Connection")
        self.lConnStat.resize(137, 50)
        self.lConnStat.setStyleSheet("background-color : transparent")
        self.lConnStat.move(137, 63)
        self.lConnStat.setAlignment(Qt.AlignCenter)
        self.lConnStat.wordWrap()

        self.bConnect = QPushButton(self)
        self.bConnect.setFont(QFont('default', 12))
        self.bConnect.setText("Connect")
        self.bConnect.resize(100, 50)
        self.bConnect.setStyleSheet("background-color : green")
        self.bConnect.move(38, 38)
        self.bConnect.clicked.connect(self.connect)
        
        self.bDinconnect = QPushButton(self)
        self.bDinconnect.setFont(QFont('default',  12))
        self.bDinconnect.setText("Disconnect")
        self.bDinconnect.resize(100, 50)
        self.bDinconnect.move(38, 88)
        self.bDinconnect.setStyleSheet("background-color : red")
        self.bDinconnect.clicked.connect(self.disconnect)

        self.lSens_1 = QLabel(self)
        self.lSens_1.setText(str(self.sensVal))
        self.lSens_1.resize(100, 25)
        self.lSens_1.move(300, 25)
        self.lSens_1.setStyleSheet("background-color : white")
        self.lSens_1.setAlignment(Qt.AlignCenter)
        
    def connect(self):
        server_old.Server.connect(server_old)
        self.connectionStat = True
        self.lConnStat.setText("Connected")
        self.fConnInd.setStyleSheet("background-color : green")
    
    def disconnect(self):
        server_old.Server.disconnect(server_old)
        self.connectionStat = False
        self.lConnStat.setText("No Connection")
        self.fConnInd.setStyleSheet("background-color : red")

    def updateLabel(self):
        QApplication.processEvents()
    
def main():
    app = QApplication(sys.argv)
    ex = window()
   
    ex.show()
    window.updateLabel(window)

    # val = 0
    # cTime = process_time()
    # if cTime > 1:
    #     val += 1
    # ex.update_lSens_1(val)
    # print(str(val))
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()    