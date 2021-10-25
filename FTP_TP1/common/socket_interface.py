import abc
import socket


class ISocket(abc.ABC):

	@abc.abstractmethod
	def send(self, data: bytes, last_send: bool = False):
		""" Envia los datos

		:param data: datos a enviar
		:type data: bytes

		"""
		pass

	@abc.abstractmethod
	def recv(self, bufsize: int):
		""" Recibe los datos

		:param bufsize: cantidad de datos a recibir
		:type bufsize: int
		:returns: los datos recibidos en forma de bytes

		"""
		pass

	def htonl(self, x):
		""" Transforma endiannes local al de la red

		:param x: entero de 4 bytes
		:returns: devuelve el entero x en endiannes de la red

		"""
		return socket.htonl(x)

	def ntohl(self, x):
		""" Transforma endiannes de la red a local

		:param x: entero de 4 bytes
		:returns: devuelve el entero x en endiannes local

		"""
		#print(socket.ntohl(x))
		return socket.ntohl(x)

	def htons(self, x):
		""" Transforma endiannes local al de la red

		:param x: entero de 2 bytes
		:returns: devuelve el entero x en endiannes de la red

		"""
		return socket.htons(x)

	def ntohs(self, x):
		""" Transforma endiannes de la red a local

		:param x: entero de 2 bytes
		:returns: devuelve el entero x en endiannes local

		"""
		return socket.ntohs(x)
