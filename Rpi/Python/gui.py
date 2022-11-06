from time import *
from tkinter import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from gui_res import *

import server

main()
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

