import os
import sys
from client_ftp.py import ClientFTP

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, '..', 'common')
sys.path.append(mymodule_dir)
from socket_tcp import SocketTCP
from socket_interface import ISocket
from comm_protocol import CommProtocol

if __name__ == "__main__":
    print("main real... deberian ser dos")
    print("upload file y download file")

    HOST = "localhost"
    PORT = 7777
    LOAD_PATH = "prueba_doc.txt"
    #STORE_PATH = "store_fname"

    with SocketTCP() as peer:
        peer.connect(HOST, PORT)
        ftp = ClientFTP(peer)

        with open(LOAD_PATH, "rb") as file:
            ftp.upload_file(file)
        
        # with open(STORE_PATH, "wb") as file:
        #     ftp.download_file(file)
