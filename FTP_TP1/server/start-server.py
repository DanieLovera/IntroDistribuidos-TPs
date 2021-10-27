import os
import sys
import argparse
from server_ftp import ServerFTP

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, '..', 'common')
sys.path.append(mymodule_dir)
from socket_tcp import SocketTCP


def parseArguments(parser):
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')
    group.add_argument('-q', '--quiet', help='decrease output verbosity', dest='verbose', action='store_false')

    parser.add_argument('-H', '--host', help='host service IP address', dest="addr", default='localhost', metavar='ADDR')
    parser.add_argument('-p', '--port', help='service port', default=7777, metavar='PORT', type=int)
    parser.add_argument('-s', '--storage', help='storage dir path', default="data_base", metavar='DIRPATH')

    transportProtocol = parser.add_mutually_exclusive_group(required=True)

    transportProtocol.add_argument('-t', '--tcp', const='tcp',
                                   required=False,
                                   help='send file over TCP protocol',
                                   dest='protocol', action='store_const')

    transportProtocol.add_argument('-w', '--saw', const='saw',
                                   required=False,
                                   help='send file over UDP protocol' +
                                   '(Stop-and-Wait)',
                                   dest='protocol', action='store_const')

    transportProtocol.add_argument('-g', '--gbn', const='gbn',
                                   required=False,
                                   help='send file over UDP protocol' +
                                   '(Go-Back-N)',
                                   dest='protocol', action='store_const')


def main():
    parser = argparse.ArgumentParser('start-server', description='<command description>')

    parseArguments(parser)
    args = parser.parse_args()
    host = args.addr
    port = args.port
    MAX_CONNECTIONS = 10
    storage_path = args.storage

    pathExist = os.path.exists(storage_path)
    if not pathExist:
        os.makedirs(storage_path)

    with SocketTCP() as listener:
        listener.bind(host, port)
        listener.listen(MAX_CONNECTIONS)
        peer = listener.accept()
        with peer:
            ftp = ServerFTP(peer)
            ftp.handle_request(storage_path)

    # descomentar:
    # if args.protocol == "tcp":
        # with SocketTCP() as listener:
        #     listener.bind(host, port)
        #     listener.listen(MAX_CONNECTIONS)
        #     peer = listener.accept()
        #     with peer:
        #         ftp = ServerFTP(peer, args.verbose)
        #         ftp.handle_request(storage_path)
    # elif args.protocol == "saw":
        # with SocketUDP() as socket:
        #    ftp = ServerFTP(socket, args.verbose)
        #    ftp.handle_request(STORE_PATH)
    # else:
        # with SocketUDP() as socket:
        #    ftp = ServerFTP(socket, args.verbose)
        #    ftp.handle_request(STORE_PATH)


if __name__ == "__main__":
    main()
