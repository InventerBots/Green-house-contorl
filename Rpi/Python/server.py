from glob import glob
import socket
from time import sleep

HOST = '0.0.0.0' # ignore server IP
PORT = 10004

tempRaw_12bit_int = []

class Server():
    Connected_Info = 0
    Connected_IP = 0
    Is_connected = False

    def __init__(self):
        super(socket, self).__init__

    def connect(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            self.Connected_Info, self.Connected_IP = s.accept()
            self.Is_connected = True
            print('Connected by', self.Connected_IP) # report connection IP for debuging

    def disconnect(self):
        if self.Is_connected:
            print('Closeing connection to', self.Connected_IP)
            self.Connected_Info.shutdown(socket.SHUT_RDWR)
            self.Is_connected = False
            self.Connected_Info.close()
        else:
            print('No connections to close')

# def connect():
    # global Connected_IP
    # global Connected_Info
    # # global Is_connected

    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #     s.bind((HOST, PORT))
    #     s.listen()
    #     Connected_Info, Connected_IP = s.accept()
    #     Is_connected = True
    #     print('Connected by', Connected_IP) # report connection IP for debuging



def read_rawTemp(sensors_to_read):
    global tempRaw_12bit_int_local
    tempRaw_12bit_int_local = []

    
    if Is_connected :
        for ind in range(1, sensors_to_read+1):
            Connected_Info.send(ind.to_bytes(2, 'big'))
            tempRaw_12bit_int_local.append(int(Connected_Info.recv(4096)))
    return tempRaw_12bit_int
try:
    tempRaw_12bit_int = tempRaw_12bit_int_local
except:
    tempRaw_12bit_int = 0