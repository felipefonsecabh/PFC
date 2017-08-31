#criar um cliente socket
import socket

class Client():
    def __init__(self,Address=('localhost',8080)):
        self.s = socket.socket()
        self.s.connect(Address)