import socket
from socket_interface import ISocket


class SocketUDP(ISocket):

    def __init__(self, host, port):
        self.__peer = None
        self.__host = host
        self.__port = port

    def __enter__(self):
        self.__peer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.close()

    def __del__(self):
        if not self.__peer:
            self.close()

    def send(self, data: bytes):
        self.__peer.sendto(data, (self.__host, self.__port))

    def recvfrom(self, bufsize: int):
        data, source = self.__peer.recvfrom(bufsize)
        return data, source

    def bind(self):
        self.__peer.bind((self.__host, self.__port))

    def close(self):
        self.__peer.close()
