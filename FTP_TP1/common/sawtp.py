import socket
import struct

@enum.unique
class Tag(enum.IntEnum):
	FLAG_ACK = 0
	SEQNUM = 1
	DATA = 2

@enum.unique
class Flag(enum.IntEnum):
	ACK = 0
	NACK = 1

class SAWTP:
	PKT_SIZE = 1024
	RTT = 100
	#FORMAT = "!HI{}s".format(PKT_SIZE)
	FORMAT = "!II" # FLAG|SEQNUM 

	def __init__(self):
		self.send_seqnum = 0
		self.recv_seqnum = 0
		self.format_dict = {Tag.FLAG_ACK: 0,
							Tag.SEQNUM: 0
							Tag.DATA: b""}

	def __acknowledged(this, ack, seqnum):
		return (ack == seqnum)

	def __pack(self, flag_ack, seqnum, data):
		packet = struct.pack(self.FORMAT, flag_ack, seqnum)
		packet += data
		return packet;

	# OJO QUE DESEMPAQUETO SOLO PARA FORMAT DICT
	def __unpack(self, packet: bytes):
		header_size = struct.calcsize(FORMAT)
	    header = struct.unpack(FORMAT, packet[:header_size])
		
		flag_ack = header[0]
		recv_seqnum = header[1]
	    recv_data = packet[header_size:]
		self.format_dict[Tag.FLAG_ACK] = flag_ack
		self.format_dict[Tag.SEQNUM] = recv_seqnum
		self.format_dict[Tag.DATA] = recv_data

	def send(this, data: bytes):
		recv_ack = 0

		socket.settimeout(self.RTT)
		for base in range(0, len(data), PKT_SIZE):
			# Transmision correcta
			chunk = data[base:(base + PKT_SIZE)]
			packet = self.pack(Flag.NACK, self.send_seqnum, chunk)

			start = now()
			socket.sendto(packet)
			end = now()
			elapsed = start - end

			socket.settimeout(self.RTT - elapsed)
			while not self.__acknowledged(recv_ack, self.recv_seqnum):
				try:
					recv_packet = socket.recvfrom(PKT_SIZE)

					format_list = self.unpack(recv_packet)



				except socket.timeout:
					socket.sendto(packet)





		while (remaining_bytes > 0):			
			pkt = pack(seqnum, data[base:base+PKT_SIZE])
			sendto(pkt, (host, port))
	
			socket.settimeout(100)
			while (ack != seqnum):
				try:
					pkt = socket.recvfrom(PKT_SIZE)[0]
					nseq, data = unpack()

				except socket.timeout:
					sendto(pkt, (host, port))

				if (ack == nseq):
					pkt = pack(nseq +1, data[base:base+PKT_SIZE])
					sendto(pkt, (host, port))
					++next_seqnum




	def recv(this, buffsize):
		pass
