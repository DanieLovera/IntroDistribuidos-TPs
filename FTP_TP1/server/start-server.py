import os
import sys
import argparse
import threading
from server_ftp import ServerFTP

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, '..', 'common')
sys.path.append(mymodule_dir)
from socket_tcp import SocketTCP
from socket_udp import SocketUDP


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


def cleanDeadClients(threads):
    for thread in threads:
        if not thread.is_alive():
            # print(threading.active_count())
            thread.join()
            # print(threading.active_count())


def start_peer(peer, storage_path, verbose):
    with peer:
        ftp = ServerFTP(peer, verbose)
        ftp.handle_request(storage_path)


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

    if args.protocol == "tcp":
        threads = []
        with SocketTCP() as listener:
            listener.bind(host, port)
            listener.listen(MAX_CONNECTIONS)
            while True:
                peer = listener.accept()
                print("arranque el theard")
                t = threading.Thread(
                    target=start_peer, args=(peer, storage_path, args.verbose)
                )
                threads.append(t)
                t.start()
                cleanDeadClients(threads)

    elif args.protocol == "saw":
        with SocketUDP(host, port, args.protocol) as socket:
            socket.bind(host, port)
            ftp = ServerFTP(socket, args.verbose)
            ftp.handle_request(storage_path)
    else:
        with SocketUDP(host, port, args.protocol) as socket:
            socket.bind(host, port)
            ftp = ServerFTP(socket, args.verbose)
            ftp.handle_request(storage_path)


if __name__ == "__main__":
    main()
