import struct
from socket_interface import ISocket


class CommProtocol:
	FORMAT = "I"

	def __init__(self, socket: ISocket):
		""" Constructor

		:param socket: recibe un socket
		:type socket: ISocket

		"""
		self.socket = socket

	def send(self, data: bytes):
		""" Envia un stream datos

		:param data: datos a enviar
		:type data: bytes

		"""
		self.__send_size(len(data))
		self.__send_chunk(data)

	def recv(self):
		""" Recibe un stream de datos

		:returns: devuelve el stream de datos leido en forma de bytes

		"""
		size = self.__recv_size()
		data = self.__recv_chunk(size)
		return data

	def __send_size(self, data_size: int):
		""" Envia una longitud fija de bytes con el tamanio
		de los datos a enviar.

		:param data_size: tamanio de los datos a enviar
		:type data_size: int

		"""
		data_size = self.socket.htonl(data_size)
		data_size = struct.pack(self.FORMAT, data_size)
		self.socket.send(data_size)

	def __send_chunk(self, data: bytes):
		""" Envia un chunk de datos

		:param data: datos a enviar

		"""
		self.socket.send(data)

	def __recv_size(self):
		""" Recibe una longitud fija de bytes con el tamanio
		del stream de datos que tiene que recibir.

		:returns: devuelve el tamanio de los datos a recibir

		"""
		fixed_length = struct.calcsize(self.FORMAT)
		data_size = self.socket.recv(fixed_length)
		print(data_size)
		if data_size:
			data_size = struct.unpack(self.FORMAT, data_size)[0]
			data_size = self.socket.ntohl(data_size)

		return data_size

	def __recv_chunk(self, bufsize):
		""" Recibe un chunk de datos

		:returns: devuelve los datos reales enviados por send

		"""
		chunk = self.socket.recv(bufsize)
		return chunk
