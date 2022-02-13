import socket               

s = socket.socket(socket.AF_INET)        
host = '169.254.1.177'# ip of raspberry pi 
port = 1024               
s.connect((host, port))
print(s.recv(1024))
s.close()