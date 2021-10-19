import socket
from socket_interface import ISocket
from sawtp import SAWTP

class SocketUDP(ISocket):

    def __init__(self, host, port):
        self.__peer = None
        self.__host = host
        self.__port = port
        self.__protocol = None

    def __enter__(self):
        self.__peer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__protocol = SAWTP(self.__peer, self.__host, self.__port)
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.close()

    def __del__(self):
        if not self.__peer:
            self.close()

    def send(self, data: bytes):
        # self.__peer.sendto(data, (self.__host, self.__port))
        self.__protocol.send(data)

    def recv(self, bufsize: int):
        # data, source = self.__peer.recvfrom(bufsize)
        # return data, source
        return self.__protocol.recv(bufsize)

    def bind(self):
        self.__peer.bind((self.__host, self.__port))

    def close(self):
        self.__peer.close()
