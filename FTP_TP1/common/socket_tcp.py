import socket
from socket_interface import ISocket


class SocketTCP(ISocket):
    SHUT_RD = socket.SHUT_RD
    SHUT_WR = socket.SHUT_WR
    SHUT_RDWR = socket.SHUT_RDWR

    def __init__(self):
        """ Constructor

        """
        self.__peer = None

    def __enter__(self):
        """  Metodo del Context Manager

        :returns: devuelve una instancia de si mismo

        """
        if not self.__peer:
            self.__peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return self

    def __exit__(self, exc_type, exc_value, tb):
        """  Metodo del Context Manager

        """
        self.shutdown(SocketTCP.SHUT_RDWR)
        self.close()

    def connect(self, host, port):
        """ Conecta un socketTCP al host y puerto indicado.

        :param host: dominio destino
        :param port: puerto destino

        """
        self.__peer.connect((host, port))

    def send(self, data: bytes):
        """ Envia todos los bytes de data.

        :param data: stream de datos a enviar.
        :type data: bytes

        """
        self.__peer.sendall(data)

    def recv(self, bufsize: int):
        """ Recibe un stream de bytes de tamanio bufsize.

        :param bufsize: tamanio del stream a recibir
        :type bufsize: int
        :returns: devuelve un stream de bytes con el contenido recibido

        """
        return self.__recvall(bufsize)

    def bind(self, host, port):
        """ Enlaza un socketTCP al host y puerto indicado

        :param host: dominio enlace
        :param port: puerto enlace

        """
        self.__peer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__peer.bind((host, port))

    def listen(self, backlog):
        """ Coloca a escuchar a un socketTCP

        :param backlog: maximo numero de clientes esperando a ser
         atendidos

        """
        self.__peer.listen(backlog)

    def accept(self):
        """ Acepta la conexion de un cliente

        :returns: devuelve una instancia socketTCP que se comunica
         con el cliente

        """
        peer, addr = self.__peer.accept()
        socket = SocketTCP()
        socket.__peer = peer
        return socket

    def shutdown(self, how):
        """ Cierra algun canal del socketTCP (envio/recepcion)

        """
        self.__peer.shutdown(how)

    def close(self):
        """ Cierra el socketTCP

        """
        self.__peer.close()

    def __recvall(self, bufsize: int):
        """ Recibe todos los bytes esperados segun bufsize

        :param bufsize: tamanio del stream a recibir
        :type bufsize: int
        :returns: devuelve un stream de bytes con el contenido recibido

        """
        data = bytearray()
        remaining_bytes = bufsize
        while (remaining_bytes > 0):
            received_stream = self.__peer.recv(remaining_bytes)
            if not received_stream:
                break
            remaining_bytes -= len(received_stream)
            data.extend(received_stream)
        return bytes(data) # si len(bytes) = 0, casi seguro es por cierre de socket en un extremo
