import math
import socket
from time import sleep

HOST = '0.0.0.0' # server IP
PORT = 10004

msg = b'Welcome!'
errorCode = -1

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.bind((HOST, PORT))
  s.listen()
  conn, addr = s.accept()
  with conn:
    print('Connected by', addr)
    while(conn):
      if (not conn) :
        break
      tempRaw_12bit_int = 0
      for i in range(1, 4): 
        # print(i)
        conn.send(i.to_bytes(2, 'big'))
        tempRaw_12bit_int = int(conn.recv(4096))
        print("12 bit value:", tempRaw_12bit_int)

        #--- temperature calculations ---#
        # convert the 12 bit analog signal to degs Kelven, then convert to degs Fahrenheit and Celsius
        R = 10000 / (4096 / tempRaw_12bit_int - 1)
        
        tempK = 1/((1/298.15)+(1/3977)*math.log(R/10000)) 
        tempF = (tempK) * (9/5) - 459.67
        tempC = (tempK) - 273.15
        print("tempK:", tempK)
        print("tempF:", tempF)
        print()
      sleep(2)
      print('\n')

def shutdown() :
  if (conn) :
    conn.send(b'SHUTDOWN')
    conn.detach()


