import os
import sys

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, '..', 'common')
sys.path.append(mymodule_dir)
from socket_udp import SocketUDP

serverName = "localhost"
serverPort = 12000

socketUDP = SocketUDP()
message = "Hola soy tu cliente!"

socketUDP.sendto(message.encode(), (serverName, serverPort))
modifiedMessage, serverAddress = socketUDP.recv(2048)
print(modifiedMessage.decode())
socketUDP.close()
