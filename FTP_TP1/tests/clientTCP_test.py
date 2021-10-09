import os
import sys

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, '..', 'common')
sys.path.append(mymodule_dir)
from socket_tcp import SocketTCP

if __name__ == "__main__":
    HOST = "localhost"
    PORT = 7777

    with SocketTCP() as peer:
        peer.connect(HOST, PORT)
        peer.send(b"Hola")
        data = peer.recv(4)
    print('Received', data)
