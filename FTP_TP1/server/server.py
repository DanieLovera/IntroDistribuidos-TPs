import os
import sys

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, '..', 'common')
sys.path.append(mymodule_dir)
from socket_tcp import SocketTCP

if __name__ == "__main__":
    HOST = "localhost"
    PORT = 7777
    MAX_CONNECTIONS = 10

    with SocketTCP() as listener:
        listener.bind(HOST, PORT)
        listener.listen(MAX_CONNECTIONS)
        peer = listener.accept()
        with peer:
            data = peer.recv(1024)
            while data:
                print('Received', data)
                peer.send(b"Hola soy tu servidor!")
                data = peer.recv(1024)
