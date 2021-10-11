# TP1: File Transfer #

## Posible diseño ##

Pueden haber 3 grandes módulos principales:
- **upload-file**: Controlara todo lo relacionado a lectura de archivo en disco previo a transferirlo.
- **download-file**: Controlara toda lo relacionado a escritura de archivo en disco luego de recibirlo.
- **start-server**: Controlara la recepcion de los archivos y su almacenamiento en disco (servidor)

### upload-file y download-file ###
Son las aplicaciones cliente que necesitamos crear para el tp y correran sobre el protocolo FTP que definamos.

- Ambas aplicaciones deberan ser independientes de las transferencias de archivos a través de la red.
- Delegaran ambos sobre un protocolo **ClientFTP** definido por nosotros
- No debe manejar nada relacionado a los sockets, unicamente tiene que especificarle al protocolo **ClienteFTP** con que servidor y puerto se vinculara.
- Utilizaran los metodos que les provea el protocolo **ClienteFTP** que deberan poder permitir enviar y recibir *chunks* de datos al protocolo.
- Una vez enviado los datos al protocolo terminan los deberes de las aplicaciones upload y download file, la responsabilidad de transferir los datos sera del protocolo **ClientFTP** que estamos utilizando.

1. ### ClientFTP ####
Este sera el protocolo de la capa de aplicación sobre la cual deben correr los programas upload-file y download-file.

- Se debera encargar de la creacion de los sockets: **SocketTCP** o **SocketUDP**.
- Debera ademas implementar los metodos necesarios para que sus clientes (upload-file y download-file) o cualquier otra aplicacion pueda transferir archivos (binarios o de lo que sea).
- Estará del lado del cliente
- **NOTA**: Queda definir como funcionara el protocolo, es decir como se relaciona con el protocolo del lado del servidor (que enviara y como lo hara)

2. ### SocketTCP ###
Esta simplemente debe ser una clase wrapper en la que realmente se configura un socket TCP de la libreria estandar

- Debe tener los metodos necesarios para enviar datos como lo hace la libreria estandar pero capaz a un nivel mas alto, sera un wraper mas simple.

3. ### SocketUDP ###
Este tambien sera un wrapper de un socket UDP real, con la salvedad de que los datos que se tengan que enviar en realidad deberan ser dirigidos a el protocolo **SAWTP** o **GBNTP** que se encargarán de hacer que nuestra implementacion de **SocketUDP** sea RDT. Cada una lo hará a su manera, si nuestro **SocketUDP** decide utilizar el protocolo **SAWTP** para enviar sus datos, deberan hacer lo haga de forma confiable, el mismo caso si se usa **GBNTP**.
- Debe implementar las funciones normales de un socket, aunque internamente no sea quien las haga (sera como un proxy de UDP).

4. ### SWATP ###
Aca si estara realmente la creacion y confiugracion de un socket de UDP de la libreria estandar de python porque **SWATP** esta corriendo encima de UDP pero asegurandose de hacer el procedimiento necesario para que los datos que vinieron del proxy SocketUDP sean enviados de forma confiable.

5. ### GBNTP ###
Mismo caso que **SWATP** pero cambiara la implementacion interna de confiabilidad sobre UDP, de resto sera igual, también funcionara sobre UDP.

6. ### start-server ###
Aplicacion del servidor que requiere el TP, es análogo a las aplicaciones del cliente en el sentido que debera gestionar el uso de archivos pero delegara sobre el protocolo FTP el envio de cada *chunk* de datos. En este caso de este lado debera correr una version de **ServerFTP**.

7. ### ServerFTP ####
Este sera el protocolo de la capa de aplicación sobre la cual debe correr el programa **start-server**. (La otra pata del protocolo logico FTP)

- Igualmente falta definir bien el formato del protocolo (supongo sera algo parecido a definir un header del protocolo) es decir que habra en cada campo del protocolo.
  
---
## Checklist ##
- [x] Implementar clase SocketTCP.
- [ ] Implementar clase SAWTP. (Recordar que va sobre UDP, aca es donde se usan los sockets estandar)
- [ ] Implementar clase GBNTP. (Recordar que va sobre UDP, aca es donde se usan los sockets estandar)
- [x] Implementar clase SocketUDP.
- [x] Implementar clase ClientFTP.
- [x] Implementar clase ServerFTP.
- [x] Implementar clase StartServer.
- [x] Implementar clase UploadFile.
- [x] Implementar clase DownLoadFile.
- [x] Crear 3 programas llamados start-server, upload-file y download-file con un *"main"* usando las clases StartServer, UpdloadFile y DownLoadFile.
- [ ] Por último cuando todo funcione, agregamos varios clientes para hacerla multithreading.
