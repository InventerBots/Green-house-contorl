import socket               

HOST = '192.168.0.220' # server IP
PORT = 80

msg = b'Hello, World!'

with socket.socket() as s:
    print("Sent,", msg)
    s.connect((HOST, PORT))
    s.sendall(msg)
    data = s.recv(1024)

print('Received', repr(data))