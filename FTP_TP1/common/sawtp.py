import socket
import struct

"""@enum.unique
class Tag(enum.IntEnum):
	FLAG_ACK = 0
	SEQNUM = 1
	DATA = 2"""

@enum.unique
class Flag(enum.IntEnum):
	ACK = 0
	NACK = 1

class SAWTP:
	PACKET_SIZE = 1024
	RTT = 100
	FORMAT = "!II" # FLAG|SEQNUM 

	def __init__(self):
		self.sender_seqnum = 0
		self.receiver_seqnum = 0


	def __pack(self, flag_ack, seqnum, data):
		packet = struct.pack(self.FORMAT, flag_ack, seqnum)
		packet += data
		return packet;

	# OJO QUE DESEMPAQUETO SOLO PARA FORMAT DICT
	def __unpack(self, packet: bytes):
		header_size = struct.calcsize(FORMAT)
	    header = struct.unpack(FORMAT, packet[:header_size])
	    data = packet[header_size:]
		
		"""flag_ack = header[0]
		recv_seqnum = header[1]
		self.format_dict[Tag.FLAG_ACK] = flag_ack
		self.format_dict[Tag.SEQNUM] = recv_seqnum
		self.format_dict[Tag.DATA] = recv_data"""
		return (header, data)

	def send(this, data: bytes):
		for base in range(0, len(data), PACKET_SIZE):
			chunk = data[base:(base + PACKET_SIZE)]
			packet = self.pack(Flag.NACK, sender_seqnum, chunk)
			socket.sendto(packet)
			start = now()

			acknowledged = False
			while not acknowledged:
				try:
					elapsed = now() - start
					socket.settimeout(self.RTT - elapsed)
					recv_packet = socket.recvfrom(PACKET_SIZE)
					header, data = self.unpack(recv_packet)

					if FLAG.ACK == header[0]:
						if header[seqnum] == sender_seqnum:
							continue

						acknowledged = True
						sender_seqnum = 1 + sender_seqnum
						sender_seqnum = sender_seqnum % 2
						socket.settimeout(None)
					else:
						packet = self.pack(Flag.ACK, receiver_seqnum, b"")

				except socket.timeout:
					socket.sendto(packet)
					start = now()

	def recv(this, buffsize):
		pass
