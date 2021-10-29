# Trabajo Práctico 1 - File Transfer

Este documento contiene instrucciones de cómo ejecutar el cliente y el servidor.

## Servidor

El servidor consta de un sólo comando `start-server`, que permite iniciar el servidor. Para correrlo, ejecutar en el directorio del archivo start-server.py:

`python3 start-server [-h] [-v | -q] [-H ADDR] [-p PORT] [-s DIRPATH] (-t | -w | -g PROTOCOL)`

Pueden utilizarse distintos flags:

`-h` , `--help` permite mostrar el mensaje de ayuda y detalle de los distintos flags.
`-v` , `--verbose` | `-q` , `--quiet` muestra detalles extra sobre el envío de archivos.
   `-H` , `--host` permite indicar el host donde se quiere levantar el servidor.
    `-p` , `--port` permite indicar el puerto donde se quiere levantar el servidor.
    `-s` , `--storage` permite indicar el directorio donde se quieren bajar los archivos.
    `-t`, `--tcp` | `-w`, `--saw` | `-g`, `--gbn` permite elegir el protocolo de capa de transporte.

## Cliente

El cliente cuenta con dos comandos distintos:

    `upload-file`: permite subir un archivo al servidor.
    `download-file`: permite descargar un archivo del servidor.

### upload-file

Para correr este módulo, ejecutar:

`$ python3 upload-file [-h] [-v | -q] [-H ADDR] [-p PORT] -s FILEPATH [-n FILENAME] (-t | -w | -g PROTOCOL)`

Pueden utilizarse distintos flags:

   `-h` , `--help` permite mostrar el mensaje de ayuda y detalle de los distintos flags.
    `-v` , `--verbose` | `-q` , `--quiet` muestra detalles extra sobre el envío de archivos.
    `-H` , `--host` permite indicar el host donde se quiere levantar el cliente.
    `-p` , `--port` permite indicar el puerto donde se quiere levantar el cliente.
    `-s` , `--src` permite indicar la ruta del archivo a enviar.
    `-n` , `--name` permite indicar el nombre con el cual el archivo queda guardado en el servidor.
    `-t`, `--tcp` | `-w`, `--saw` | `-g`, `--gbn` permite elegir el protocolo de capa de transporte.

### download-file

Para correr este módulo, ejecutar:

`$ python3 download-file [-h] [-v | -q] [-H ADDR] [-p PORT] [-d FILEPATH] -n FILENAME (-t | -w | -g PROTOCOL)`

Pueden utilizarse distintos flags:

   `-h` , `--help` permite mostrar el mensaje de ayuda y detalle de los distintos flags.
    `-v` , `--verbose` | `-q` , `--quiet` muestra detalles extra sobre el envío de archivos.
    `-H` , `--host` permite indicar el host donde se quiere levantar el cliente.
    `-p` , `--port` permite indicar el puerto donde se quiere levantar el cliente.
    `-s` , `--dst` permite indicar la ruta donde será guardado el archivo descargado.
    `-n` , `--name` permite indicar el nombre del archivo alojado en el servidor a descargar.
    `-t`, `--tcp` | `-w`, `--saw` | `-g`, `--gbn` permite elegir el protocolo de capa de transporte.