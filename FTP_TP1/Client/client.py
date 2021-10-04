import socket


if __name__ == "__main__":
    HOST = "localhost"
    PORT = 7777

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as peer:
        peer.connect((HOST, PORT))
        peer.sendall(b"Hola soy tu cliente!")
        data = peer.recv(1024)
    print('Received', data)
