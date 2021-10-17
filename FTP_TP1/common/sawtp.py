import socket
import struct

# ACK = 1 es un ack
# ACK = 0 caso contrario

class SAWTP:
	PKT_SIZE = 512


	def __init__(self):
		pass

	# seq | data 

	def send(this, data: bytes):
		remaining_bytes = len(data)
		base = 0
		ack = 0
		next_seqnum = 0

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




	def make_pkt(self, seqnum, data):
		pkt = struct.pack(self.FORMAT, seqnum, data)
		return pkt;

	def recv(this):
		pass
