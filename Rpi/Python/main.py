import time
import threading
import sys

import gui

if __name__ == '__main__':
    gui.server.Server.connect(gui.server)
    startTime = time.time_ns()
    gui.server.Server.read_rawTemp(gui.server, 3)
    endTime = time.time_ns()
    gui.server.Server.disconnect(gui.server)
    print(endTime-startTime)
    # app = gui.QApplication([])
    # window = gui.MainWindow()
    # app.exec()