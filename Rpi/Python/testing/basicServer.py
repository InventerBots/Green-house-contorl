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
    while True:
      temp = 0
      for i in range(1, 4): 
        print(i)
        conn.send(i.to_bytes(2, 'big'))
        temp = int(conn.recv(4096))
        print(temp)
        if (int(temp) > 10000) :
          conn.send(errorCode.to_bytes(2, 'big'))
          print("bad reading")
      
      sleep(2)

        
    # while True:
    #   data = conn.recv(1024)
    #   if not data:
    #     break
    #   print("Receved: ", data)
    #   print("Sent: ", msg)
    #   conn.sendall(msg)

