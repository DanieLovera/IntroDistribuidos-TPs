import socket

class SocketUDP:

    def __init__(self):
        self.__peer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    #def __enter__(self):
       # self.__peer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
       # return self

    def __exit__(self, exc_type, exc_value, tb):
        self.close()

    def __del__(self):
        if not self.__peer:
            self.close()

    def sendto(self, data: bytes, address):
        self.__peer.sendto(data, address)

    def recvfrom(self, bufsize: int):
        data, source = self.__peer.recvfrom(bufsize)
        return data, source

    def bind(self, host, port):
        self.__peer.bind((host, port))

    def close(self):
        self.__peer.close()