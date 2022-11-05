from time import sleep
import threading

import server

def ServerTask():
  global serverRunning
  serverRunning = True
  x = 0
  server.connect()
  while serverRunning:
    server.read_rawTemp(3)
    print(server.tempRaw_12bit_int_local)
    if x == 6:
      break
    x += 1
    sleep(2)
  
  server.disconnect()

if __name__ == '__main__':
  serverTask = threading.Thread(ServerTask())
  
  serverTask.start()
  
  serverTask.join()
