import os
import sys

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, '..', 'common')
sys.path.append(mymodule_dir)
from socket_tcp import SocketTCP

if __name__ == "__main__":
    print("main real... deberian ser server-start")

