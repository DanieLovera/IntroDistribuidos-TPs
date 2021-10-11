import os
import sys

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, '..', 'common')
sys.path.append(mymodule_dir)
from socket_tcp import SocketTCP
from socket_interface import ISocket
from comm_protocol import CommProtocol

def do_send(comm_protocol: CommProtocol):
    msg = "Npi"
    comm_protocol.send(msg.encode())

def do_recv(comm_protocol: CommProtocol):
    return comm_protocol.recv().decode()

if __name__ == "__main__":

    HOST = "localhost"
    PORT = 7777
    MAX_CONNECTIONS = 10

    with SocketTCP() as listener:
        listener.bind(HOST, PORT)
        listener.listen(MAX_CONNECTIONS)
        peer = listener.accept()
        with peer:
            comm_protocol = CommProtocol(peer)
            data = do_recv(comm_protocol)
            do_send(comm_protocol)
            print('Recibi el mensaje:', data)
