import socket
from socket_interface import ISocket
from sawtp import SAWTP
from gbntp import GBNTP


class SocketUDP(ISocket):

    def __init__(self, host, port, protocol):
        self.__peer = None
        self.__host = host
        self.__port = port
        self.__protocol_string = protocol
        self.__protocol = None

    def __enter__(self):
        self.__peer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if(self.__protocol_string == "gbn"):
            self.__protocol = GBNTP(self.__peer)
        else:
            self.__protocol = SAWTP(self.__peer)
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.close()

    def __del__(self):
        if not self.__peer:
            self.close()

    def send(self, data: bytes):
        self.__protocol.send(data, self.__host, self.__port)

    def recv(self, bufsize: int):
        data, source = self.__protocol.recv(bufsize)
        self.__host = source[0]
        self.__port = source[1]
        return data

    def bind(self, host, port):
        self.__peer.bind((host, port))

    def close(self):
        self.__peer.close()
