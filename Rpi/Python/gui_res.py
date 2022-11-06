import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from time import *
import server
class window(QWidget):
    def __init__(self):
        super(window, self).__init__()
        self.resize(1200, 480)
        self.setWindowTitle("PyQt5")
        self.initUI()

    def initUI(self):
        self.label = QLabel(self)
        self.label.move(100, 0)
        if server.Server.Is_connected == True:
            self.label.setText(str(server.Server.Connected_IP))
        else:
            self.label.setText("No connection")

        self.bConnect = QPushButton(self)
        self.bConnect.setText("Connect")
        self.bConnect.clicked.connect(self.connect)
        self.bConnect.move(0, 0)
        
        self.bDinconnect = QPushButton(self)
        self.bDinconnect.setText("Disconnect")
        self.bDinconnect.clicked.connect(self.disconnect)
        self.bDinconnect.move(0, 20)
        
    def connect(self):
        server.Server.connect(self)
    
    def disconnect(self):
        server.Server.disconnect(self)

def main():
    app = QApplication(sys.argv)
    ex = window()
   
    ex.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()    