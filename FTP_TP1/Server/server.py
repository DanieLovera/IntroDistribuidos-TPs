import socket


if __name__ == "__main__":
    HOST = "localhost"
    PORT = 7777
    MAX_CONNECTIONS = 10

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((HOST, PORT))
        listener.listen(MAX_CONNECTIONS)
        peer, ret_address = listener.accept()
        with peer:
            # print('Connected by', ret_address)
            data = peer.recv(1024)
            while data:
                print('Received', data)
                peer.sendall(b"Hola soy tu servidor!")
                data = peer.recv(1024)
