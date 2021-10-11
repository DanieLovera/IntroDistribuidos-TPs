import os
import sys
import argparse
from client_ftp import ClientFTP

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, '..', 'common')
sys.path.append(mymodule_dir)
from socket_tcp import SocketTCP

def parseArguments(parser):
    group = parser.add_mutually_exclusive_group(required=False)

    group.add_argument('-v', '--verbose', dest='verbose',
                       required=False, help='increase output verbosity',
                       action='store_true')

    group.add_argument('-q', '--quiet', dest='verbose',
                       required=False, help='decrease output verbosity',
                       action='store_false')

    parser.set_defaults(verbose=False)

    parser.add_argument('-H', '--host', type=str, default='localhost',
                        required=False, help='server IP address', dest='addr')

    parser.add_argument('-p', '--port', type=int, default=7777,
                        required=False, help='server port')

    parser.add_argument('-s', '--src', type=str, default='./archivo',
                        required=True, help='source file path',
                        dest='filepath')

    parser.add_argument('-n', '--name', type=str, default='archivo',
                        required=False, help='file name', dest='filename')


def main():
    parser = argparse.ArgumentParser(description='Envía un archivo al' +
                                     ' servidor para ser guardado' +
                                     ' con el nombre asignado')
    parseArguments(parser)
    args = parser.parse_args()
    host = args.addr
    port = args.port
    fpath = args.filepath
    fname = args.filename

    with SocketTCP() as peer:
        peer.connect(host, port)
        ftp = ClientFTP(peer)

        with open(fpath, "rb") as file:
            ftp.upload_file(file, fname)

if __name__ == "__main__":
    main()
