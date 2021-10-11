import abc
import socket


class ISocket(abc.ABC):

	@abc.abstractmethod
	def send(self, data: bytes):
		pass

	@abc.abstractmethod
	def recv(self, bufsize: int):
		pass

	def htonl(self, x):
		return socket.htonl(x)

	def ntohl(self, x):
		return socket.ntohl(x)
