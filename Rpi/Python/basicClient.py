import socket               

HOST = '169.254.80.147' # server IP
PORT = 2046

msg = b'Hello, World!'

with socket.socket() as s:
    print("Sent,", msg)
    s.connect((HOST, PORT))
    s.sendall(msg)
    data = s.recv(1024)

print('Received', repr(data))