import abc
import socket


class ISocket(abc.ABC):

	@abc.abstractmethod
	def send(self, data: bytes):
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

		"""
		pass

	def htonl(self, x):
		""" Transforma endiannes local al de la red

		:param x: entero de 4 bytes

		"""
		return socket.htonl(x)

	def ntohl(self, x):
		""" Transforma endiannes de la red a local

		:param x: entero de 4 bytes

		"""
		return socket.ntohl(x)
