from time import sleep
import threading
import sys

import server
import gui_res

def ServerTask():
  while gui_task.is_alive:
    if server.Server.Is_connected:
      gui_res.window.sensVal += 1
      sleep(1)

def GuiTask():
  app = gui_res.QApplication(sys.argv)
  ex = gui_res.window()
  ex.show()
  sys.exit(app.exec_())

if __name__ == '__main__':
  gui_task = threading.Thread(target=GuiTask)
  serverTask = threading.Thread(target=ServerTask)

  gui_task.start()
  serverTask.start()


  # serverTask.join()
  