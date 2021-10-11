import os
import sys
import argparse

script_dir = os.path.dirname(__file__)
myModule_dir = os.path.join(script_dir, '..', 'common')
sys.path.append(myModule_dir)

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

    parser.add_argument('-d', '--dst', type=str, default='./downloads',
                        required=True, help='destination file path',
                        dest='filepath')

    parser.add_argument('-n', '--name', type=str, default='archivo',
                        required=False, help='file name', dest='filename')


def main():
    parser = argparse.ArgumentParser(description='Solicita y recibe un archivo del servidor')

    parseArguments(parser)
    args = parser.parse_args()

    # Para testear la escritura
    file = open("testText.txt", "r")
    content = file.read()
    file.close()

    """
    Del llamado recibo el nombre del archivo. 
    la direccion donde va a ser guardado.  
    el puerto a conectarme 
    y el host
    """

    # Verifico si existe el path
    fileDir = os.path.dirname(args.filepath)
    pathExist = os.path.exists(fileDir)

    # Si no existe lo creo
    if not pathExist:
        os.makedirs(fileDir)


    # conexion con el ftp client

    # fileTransferProtocol = FTP()
    # haceme el download del archivo x
    # fileTransferProtocol.sendAll(args.name)

    # with SocketTCP() as peer:
    #    # peer.connect(args.host, args.port)
    #    with open(args.filepath, 'w') as downloadedFile:
    #        for line in peer.recv(data):
    #            downloadedFile.write(str(line))



    # codigo de prueba de funcionalidad
    # leemos un archivo linea a linea y lo escribimos en el directorio
    with open(args.filepath, 'w') as downloadedFile:
        for data in content:
            downloadedFile.write(str(data))
            #print(data)


if __name__ == "__main__":
    main()
