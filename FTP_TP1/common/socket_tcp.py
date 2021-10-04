import socket


class SocketTCP:
    SHUT_RD = socket.SHUT_RD
    SHUT_WR = socket.SHUT_WR
    SHUT_RDWR = socket.SHUT_RDWR

    def __init__(self):
        self.__peer = None

    def __enter__(self):
        self.__peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.shutdown(SocketTCP.SHUT_RDWR)
        self.close()

    def __del__(self):
        if not self.__peer:
            self.shutdown(SocketTCP.SHUT_RDWR)
            self.close()

    def connect(self, host, port):
        self.__peer.connect((host, port))

    def send(self, data: bytes):
        self.__peer.sendall(data)

    def recv(self, bufsize: int):
        data = self.__peer.recv(bufsize)
        return data

    def bind(self, host, port):
        self.__peer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__peer.bind((host, port))

    def listen(self, backlog):
        self.__peer.listen(backlog)

    def accept(self):
        peer, addr = self.__peer.accept()
        return peer

    def shutdown(self, how):
        self.__peer.shutdown(how)

    def close(self):
        self.__peer.close()
