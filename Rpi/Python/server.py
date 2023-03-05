import socket
import time

class TCPServer:
    def __init__(self, host='192.168.1.50', port=10004):
        # super().__init__()
        
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        # self.server_socket.listen(5)
        
        self.tempRaw_12bit_int = []

    def acceptConnection(self):
        self.server_socket.listen(5)
        print('Server listening on {}:{}'.format(self.host, self.port))
        return self.server_socket.accept()
        
    def openConnection(self, socket, sensors_to_read):
        if type(socket) is not tuple:
            raise Exception('Socket not doses not exist!')
        client_socket, client_address = socket
        self.tempRaw_12bit_int.clear()
        
        for ind in range(1, sensors_to_read+1):
            client_socket.send(ind.to_bytes(2, 'big'))
            self.tempRaw_12bit_int.append(int(client_socket.recv(4096)))
        print('reading')
        
    def disconnect(self):
        print('Server shutting down')
        self.server_socket.shutdown(socket.SHUT_RD)
        self.server_socket.close()

if __name__ == '__main__':
    server = TCPServer()
    try:
        client_connection = server.acceptConnection()
        for x in range(0, 30):
            server.openConnection(client_connection, 3)
            time.sleep(0.25)
        server.disconnect()
    except KeyboardInterrupt:
        server.disconnect()
