import enum
import os
import sys
import threading
import struct

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, '..', 'common')
sys.path.append(mymodule_dir)

from comm_protocol import CommProtocol
from socket_interface import ISocket


@enum.unique
class Opcode(enum.IntEnum):
    UPLOAD = 0
    DOWNLOAD = 1
    EOF = 2
    NEOF = 3


class ServerFTP:
    FORMAT = "H"
    CHUNK_SIZE = 1024 * 1024

    def __init__(self, socket: ISocket, verbose):
        self.socket = socket
        self.commProtocol = CommProtocol(socket)
        self.verbose = verbose

    def handle_request(self, store_path: str):
        opcode = self.__recv_opcode()
        if (opcode == Opcode.UPLOAD):
            self.__handle_upload_request(store_path)

        elif (opcode == Opcode.DOWNLOAD):
            self.__handle_download_request(store_path)

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

    def __recv_fname(self):
        fname = self.commProtocol.recv()
        decoded_fname = fname.decode()
        return decoded_fname

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

    def __handle_upload_request(self, store_path: str):
        sem = threading.Semaphore()
        sem.acquire()
        fname = self.__recv_fname()
        path = store_path + "/" + fname
        with open(path, "wb") as file:
            self.__recv_file(file)
        sem.release()

    def __handle_download_request(self, store_path: str):
        fname = self.__recv_fname()
        path = store_path + "/" + fname
        with open(path, "rb") as file:
            self.__send_file(file)
            self.__send_opcode(Opcode.EOF)
