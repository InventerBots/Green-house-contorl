from time import sleep, time
import threading
import sys

import gui

if __name__ == '__main__':
    app = gui.QApplication([])
    window = gui.MainWindow()
    app.exec_()