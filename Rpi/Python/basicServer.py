import socket

HOST = '0.0.0.0' # server IP
PORT = 10004

msg = b'Welcome!'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.bind((HOST, PORT))
  s.listen()
  conn, addr = s.accept()
  with conn:
    print('Connected by', addr)
    while True:
      data = conn.recv(1024)
      if not data:
        break
      print("Receved: ", data)
      print("Sent: ", msg)
      conn.sendall(msg)

