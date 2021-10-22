import socket
from time import perf_counter as now


def next(seq_number):
    return bytes(int(seq_number) + 1)


class GBNTP:
    RTT = 1
    WINDOW_SIZE = 4
    SEQ_NUM_SIZE = 4
    MAX_DATAGRAM_SIZE = 64 * 1024

    def __init__(self, socket, host, port):
        self.sender_base = b'1'
        self.sender_next_seqnum = b'1'
        self.receiver_seqnum = b'0'
        self.socket = socket
        self.not_acknowledged = []
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
        if self.sender_next_seqnum < self.sender_base + self.WINDOW_SIZE:
            self.not_acknowledged[self.sender_next_seqnum] = self.__pack(self.sender_next_seqnum, _data)
            sent = self.socket.sendto(self.not_acknowledged[self.sender_next_seqnum], (self.__host, self.__port))
            if self.sender_next_seqnum == self.sender_base:
                start = now()

            self.sender_next_seqnum = next(self.sender_next_seqnum)
        else:
            # A tratarse luego la idea seria manejarlo con un while y una cola
            # Osea el sender sera bloqueante solo si la ventana esta llena
            raise Exception

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
        correct_seq_numb = False
        while not correct_seq_numb:
            pkt_received, source = self.socket.recvfrom(buffsize + self.SEQ_NUM_SIZE)
            seq_num_received, data_received = self.__unpack(pkt_received)

            if seq_num_received == self.receiver_seqnum:
                pkt = self.__pack(self.receiver_seqnum, b'')
                self.socket.sendto(pkt, source)
                self.receiver_seqnum = toggled(self.receiver_seqnum)
                correct_seq_numb = True
            else:
                pkt = self.__pack(toggled(self.receiver_seqnum), b'')
                self.socket.sendto(pkt, source)

        return data_received
