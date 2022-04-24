import math
import socket

OFFSET = 1.0769876281322618901231464338237
HOST = '0.0.0.0' # server IP
PORT = 10004

RELAY_ON=bytes(1)
RELAY_OFF=bytes(0)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.bind((HOST, PORT))
  s.listen()
  conn, addr = s.accept()
  with conn:
    print('Connected by', addr)
    while True:
      #--- temperature calculations ---#
      tempK=1/((1/298.15)+(1/3977)*math.log((10000/(1023/int(conn.recv(1023))-1))/10000))
      tempF=(tempK-273.15)*(9/5)+32
      print("Receved: ", tempF)

      #--- fan control ---#
      if tempF>80 :
        conn.send(RELAY_ON)
        print("on")
      else :
        conn.send(RELAY_OFF)
        print("off")
