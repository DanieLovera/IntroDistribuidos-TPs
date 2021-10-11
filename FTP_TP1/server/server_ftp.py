import enum
import os
import sys
import struct

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, '..', 'common')
sys.path.append(mymodule_dir)
from comm_protocol import CommProtocol

@enum.unique
class Opcode(enum.IntEnum):
	UPLOAD = 0
	DOWNLOAD = 1
	EOF = 2
	NEOF = 3
	#LISTAR = 4
	#CUALQUIER OTRO COMANDO QUE HAGA FALTA


class ServerFTP:
	FORMAT = "h"

	def __init__(self, socket: ISocket):
		self.socket = socket
		self.commProtocol = CommProtocol(socket)


	# oo handle_request(self, store_path)
	def recv_request(self, store_path):
		# opcode = self.recv_opcode()
		# if (opcode == Opcode.UPLOAD):
		#	 file_name = self.commProtocol.recv()
		#
		#	 path = ruta store + filename
		#	 file = openfile(path, "wb")
		#	 request = StoreRequest(file)
		# 	 oooo... downloadfile(file)
		#
		# else if (opcode == Opcode.DOWNLOAD):
		#	 file_name = self.commProtocol.recv()
		#
		#	 path = ruta store + filename
		#	 file = openfile(path, "rb")
		#	 request = LoadRequest(file)
		#    oooo... uploadfile(file) 
		#
		# else if (opcode == Opcode.LIST): 
		# 	 enviar todos los documentos en el store path
		#
		#return request 

	def __upload_file(self, file):
		file_name = self.commProtocol.recv()
		# Logica para enviar datos del archivo
		# a medida se va leyendo, siempre tiene que enviar otro
		# mensaje adicional ademas de los datos para que indique fin de archivo.

		# while (!file(eof)) {
		# 	self.__send_opcode(Opcode.NEOF)
		#
		#	----- Logica para leer data de file -----
		#
		#   self.commProtocol.send(data)
		# }
		# self.__send_opcode(Opcode.EOF)

	def __download_file(self, file):
		file_name = self.commProtocol.recv()
		# Logica para recibir datos del servidor y guardarlos
		# en el archivo a medida se va leyendo pero tambien
		# debera ir recibiendo siempre bytes fijos para verificar
		# fin de archivo.

		# sopcode = self.__recv_opcode()
		# while (sopcode != Opcode.EOF) {
		#	data = self.commProtocol.recv()
		#
		# 	----- Logica para escribir data sobre file -----
		#
		#	sopcode = self.__recv_opcode() # vuelvo a recibir opcode
		# }

	def __send_opcode(self, opcode: Opcode):
		sopcode = int(opcode)
		sopcode = self.socket.htons(sopcode)
		sopcode = struct.pack(self.FORMAT, sopcode)
		self.commProtocol.send(sopcode)

	def __recv_opcode(self):
		sopcode = self.commProtocol.recv()
		sopcode = struct.unpack(self.FORMAT, sopcode)[0]
		sopcode = self.socket.ntohs(sopcode)
		return sopcode
