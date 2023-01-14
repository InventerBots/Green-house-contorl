import socket
from math import log

HOST = '0.0.0.0' # ignore server IP
PORT = 10004

Is_connected = False
tempRaw_12bit_int = []

class Server():
    Connected_Info = 0
    Connected_IP = 0

    def __init__(self):
        super(socket, self).__init__

    def connect(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            self.Connected_Info, self.Connected_IP = s.accept()
            self.Is_connected = True
            print('Connected by', self.Connected_IP) # report connection IP for debuging
            return self.Connected_IP

    def disconnect(self):
        if self.Is_connected:
            print('Closeing connection to', self.Connected_IP)
            self.Connected_Info.shutdown(socket.SHUT_RDWR)
            self.Is_connected = False
            self.Connected_Info.close()
        else:
            print('No connections to close')
    
    def read_rawTemp(self, sensors_to_read):
        tempRaw_12bit_int.clear()
        if self.Is_connected == False:
            return -1
            
        for ind in range(1, sensors_to_read+1):
            self.Connected_Info.send(ind.to_bytes(2, 'big'))
            tempRaw_12bit_int.append(int(self.Connected_Info.recv(4096)))
        return tempRaw_12bit_int

    def sendComand(self, code):
        if self.Is_connected == False:
            return -1
        self.Connected_Info.send(int(code).to_bytes(2, 'big'))

    # ---------- Temp converters ---------- #

    def convertRawToDeg_K (rawTemp):
        try:
            R = 10000 / (4096 / int(rawTemp) - 1)
            return 1/((1/298.15)+(1/3977)*log(R/10000))
        except:
            Exception()
    
    def convertRawToDeg_F (rawTemp):
        try:
            R = 10000 / (4096 / int(rawTemp) - 1)
            tempK = 1/((1/298.15)+(1/3977)*log(R/10000)) 
            return (tempK) * (9/5) - 459.67
        except:
            Exception()

    def convertRawToDeg_C (rawTemp):
        try:
            R = 10000 / (4096 / int(rawTemp) - 1)
            tempK = 1/((1/298.15)+(1/3977)*log(R/10000))
            return (tempK) - 273.15
        except:
            Exception()