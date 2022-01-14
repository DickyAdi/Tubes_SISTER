import socket
import pickle

class Network:
    def __init__(self):
        # INISIALISASI SOCKET#
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # HOST ADDRESS YG DIGUNAKAN ADALAH IPv4 DEVICE YANG MENJADI SERVER#
        self.server = "26.137.125.5"
        self.port = 5005
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(4096).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(4096*2))
        except socket.error as e:
            print(e)