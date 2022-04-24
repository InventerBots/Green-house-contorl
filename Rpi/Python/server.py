import socket

OFFSET = 1.0769876281322618901231464338237
HOST = '0.0.0.0' # server IP
PORT = 10004

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.bind((HOST, PORT))
  s.listen()
  conn, addr = s.accept()
  with conn:
    print('Connected by', addr)
    while True:
      rawTemp=int(conn.recv(1023))
      tempR=10000/(1023/rawTemp-1)
      tempK=1/((1/298.15)+(1/3977))*OFFSET
      tempF=(tempK-273.15)*(9/5)+32
      print("Receved: ", tempF)
