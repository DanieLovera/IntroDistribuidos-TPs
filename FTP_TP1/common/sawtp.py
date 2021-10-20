import socket
from time import perf_counter as now


def toggled(seq_number):
    if seq_number == b'0':
        return b'1'
    return b'0'


class SAWTP:
    RTT = 1
    SEQ_NUM_SIZE = 1
    MAX_DATAGRAM_SIZE = 64 * 1024

    def __init__(self, socket, host, port):
        self.sender_seqnum = b'0'
        self.receiver_seqnum = b'0'
        self.socket = socket
        self.__host = host
        self.__port = port

    def __pack(self, seqnum, data: bytearray):
        return seqnum + data

    def __unpack(self, packet: bytearray):
        seq_num = packet[:self.SEQ_NUM_SIZE]
        data = packet[self.SEQ_NUM_SIZE:]
        return seq_num, data

    def send(self, data: bytes):
        _data = bytearray(data)
        pkt = self.__pack(self.sender_seqnum, _data)
        sent = self.socket.sendto(pkt, (self.__host, self.__port))
        start = now()
        acknowledged = False

        while not acknowledged:
            try:
                elapsed = now() - start
                self.socket.settimeout(self.RTT - elapsed)
                pkt_received, _ = self.socket.recvfrom(self.SEQ_NUM_SIZE)
                seq_num_received, _ = self.__unpack(pkt_received)

                if seq_num_received == self.sender_seqnum:
                    self.socket.settimeout(None)
                    self.sender_seqnum = toggled(self.sender_seqnum)
                    acknowledged = True

            except socket.timeout:
                sent = self.socket.sendto(pkt, (self.__host, self.__port))
                start = now()

        return sent

    def recv(self, buffsize):
        pkt_received, source = self.socket.recvfrom(buffsize + self.SEQ_NUM_SIZE)
        seq_num_received, data_received = self.__unpack(pkt_received)

        if seq_num_received == self.receiver_seqnum:
            pkt = self.__pack(self.receiver_seqnum, b'')
            self.socket.sendto(pkt, source)
            self.receiver_seqnum = toggled(self.receiver_seqnum)
        else:
            pkt = self.__pack(toggled(self.receiver_seqnum), b'')
            self.socket.sendto(pkt, source)

        return data_received
