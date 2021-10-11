import os
import sys
from client_ftp import ClientFTP

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, '..', 'common')
sys.path.append(mymodule_dir)
from socket_tcp import SocketTCP

if __name__ == "__main__":
    print("main real... deberian ser dos")
    print("upload file y download file")

    HOST = "localhost"
    PORT = 7777
    LOAD_PATH = "prueba_doc.txt" # 14 caracteres
    STORE_PATH = "caca.txt"

    with SocketTCP() as peer:
        peer.connect(HOST, PORT)
        ftp = ClientFTP(peer)

        with open(LOAD_PATH, "rb") as file:
           ftp.upload_file(file)
        
        #with open(STORE_PATH, "wb") as file:
        #    ftp.download_file(file)
