import os
import sys

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, '..', 'common')
sys.path.append(mymodule_dir)
from socket_udp import SocketUDP

serverPort = 12000
clientName = "localhost"

socketUDP = SocketUDP()

socketUDP.bind("localhost", serverPort)

message, clientAddress = socketUDP.recv(2048)
print(message.decode())
socketUDP.sendto(message, clientAddress)
socketUDP.close()
