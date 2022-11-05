from time import *
from tkinter import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from gui_res import *

import server

window.__init__

def close():
    server.disconnect()

def window():
    app = QApplication(sys.argv)
    w = QWidget()
    b = QLabel(w)
    b.setText("Hello World!")
    w.setGeometry(100, 100, 200, 50)
    b.move(50, 20)
    w.setWindowTitle("PyQt5 test")
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    window()
# def test():
#     moniterWindow = Tk()
#     moniterWindow.minsize(250, 180)
#     server.connect()
#     temp = StringVar()
#     sensor = Label(moniterWindow, relief='solid', textvariable=temp)
#     sensor.pack()
    
#     server.read_rawTemp(3)
#     temp.set(str(server.tempRaw_12bit_int_local[1]))
    
#     exitServer = Button(moniterWindow, text="exit server", command=close)
#     exitServer.pack()
#     moniterWindow.mainloop()

# master = Tk()
# master.minsize(800, 400)
# master.title('Green houes control')
# startServer = Button(master, text='start server', command=test)
# startServer.pack()

# master.mainloop()   

