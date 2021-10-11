import os
import sys
from server_ftp.py import ServerFTP

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, '..', 'common')
sys.path.append(mymodule_dir)
from socket_tcp import SocketTCP
from socket_interface import ISocket
from comm_protocol import CommProtocol

if __name__ == "__main__":

    HOST = "localhost"
    PORT = 7777
    STORE_PATH = "./data_base"
    MAX_CONNECTIONS = 10

    with SocketTCP() as listener:
        listener.bind(HOST, PORT)
        listener.listen(MAX_CONNECTIONS)
        peer = listener.accept()
        with peer:
            ftp = ServerFTP(peer)
            ftp.handle_request(STORE_PATH)

    with SocketUDP() as socket:
        ftp = ServerFTP(socket)
        ftp.handle_request(STORE_PATH)
