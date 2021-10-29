import enum
import os
import sys
import struct

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, '..', 'common')
sys.path.append(mymodule_dir)

from socket_interface import ISocket
from comm_protocol import CommProtocol


@enum.unique
class Opcode(enum.IntEnum):
    UPLOAD = 0
    DOWNLOAD = 1
    EOF = 2
    NEOF = 3
    #LISTAR = 4
    # CUALQUIER OTRO COMANDO QUE HAGA FALTA


class ClientFTP:
    FORMAT = "H"
    CHUNK_SIZE = 1024 * 1024

    def __init__(self, socket: ISocket, verbose):
        self.socket = socket
        self.commProtocol = CommProtocol(socket)
        self.verbose = verbose

    # RECIBE UN ARCHIVO BINARIO ABIERTOOOO PARA LECTURA!
    def upload_file(self, file, fname):
        print("Enviando archivo.")
        self.__send_opcode(Opcode.UPLOAD)
        self.__send_fname(fname)
        self.__send_file(file)
        self.__send_opcode(Opcode.EOF)
        print("Archivo enviado.")

    # RECIBE UN ARCHIVO BINARIO ABIERTOOOO PARA ESCRITURA!
    def download_file(self, file, fname):
        print("Recibiendo archivo.")
        self.__send_opcode(Opcode.DOWNLOAD)
        self.__send_fname(fname)
        self.__recv_file(file)
        print("Archivo recibido.")

    def __send_opcode(self, opcode: Opcode):
        sopcode = int(opcode)
        sopcode = self.socket.htons(sopcode)
        sopcode = struct.pack(self.FORMAT, sopcode)
        self.commProtocol.send(sopcode)

    def __recv_opcode(self):
        sopcode = self.commProtocol.recv()
        sopcode = struct.unpack(self.FORMAT, sopcode)[0]
        sopcode = self.socket.ntohs(sopcode)
        return sopcode

    def __send_fname(self, fname):
        encoded_fname = fname.encode()
        self.commProtocol.send(encoded_fname)

    def __send_chunk(self, chunk: bytes):
        self.__send_opcode(Opcode.NEOF)
        self.commProtocol.send(chunk)

    def __send_file(self, file):
        chunk = file.read(self.CHUNK_SIZE)
        while chunk:
            if self.verbose:
                print("Enviados " + str(file.tell()) + " bytes de " +
                      str(os.stat(file.fileno()).st_size))
            self.__send_chunk(chunk)
            chunk = file.read(self.CHUNK_SIZE)

    def __recv_file(self, file):
        sopcode = self.__recv_opcode()
        while sopcode != Opcode.EOF:
            chunk = self.commProtocol.recv()
            file.write(chunk)
            sopcode = self.__recv_opcode()
