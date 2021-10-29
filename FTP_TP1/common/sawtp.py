import socket
from timer import Timer
from time import perf_counter as now


def toggled(seq_number):
    if seq_number == b'0':
        return b'1'
    return b'0'


class SAWTP:
    SEQ_NUM_SIZE = 1
    MAX_DATAGRAM_SIZE = 64000    # 64kb
    MAX_TIMEOUTS = 6

    def __init__(self, socket):
        self.sender_seqnum = b'0'
        self.receiver_seqnum = b'0'
        self.socket = socket
        self.timeout = Timer()

    def __pack(self, seqnum, data: bytearray):
        return seqnum + data

    def __unpack(self, packet: bytearray):
        seq_num = packet[:self.SEQ_NUM_SIZE]
        data = packet[self.SEQ_NUM_SIZE:]
        return seq_num, data

    def _send_a_packet(self, data: bytearray, host, port, last_send):
        pkt = self.__pack(self.sender_seqnum, data)
        sent = self.socket.sendto(pkt, (host, port))
        start = now()
        acknowledged = False
        timeouts = 0
        if last_send:
            print("----Last send----")
        while not acknowledged:
            try:
                timeout = self.timeout.getTimeout() - (now() - start)
                self.socket.settimeout(timeout)
                pkt_received, _ = self.socket.recvfrom(self.SEQ_NUM_SIZE)
                seq_num_received, _ = self.__unpack(pkt_received)

                print("waiting:")
                print(self.sender_seqnum)
                print("received:")
                print(seq_num_received)
                if seq_num_received == self.sender_seqnum:
                    self.timeout.calculateTimeout(now() - start)
                    self.socket.settimeout(None)
                    self.sender_seqnum = toggled(self.sender_seqnum)
                    acknowledged = True

            except socket.timeout:
                if last_send:
                    timeouts += 1
                print("timeout")
                self.timeout.timeout()
                sent = self.socket.sendto(pkt, (host, port))
                start = now()

            if last_send and timeouts >= self.MAX_TIMEOUTS:
                self.sender_seqnum = toggled(self.sender_seqnum)
                self.socket.settimeout(None)
                break

        return sent

    def send(self, data: bytes, host, port):
        _data = bytearray(data)
        sent = 0

        for i in range(0, len(_data), self.MAX_DATAGRAM_SIZE):
            last_send = False

            if i + self.MAX_DATAGRAM_SIZE > len(_data):
                last_send = True

            sent += self._send_a_packet(
                _data[i:min(i + self.MAX_DATAGRAM_SIZE, len(_data))],
                host,
                port,
                last_send
            )

        self.socket.settimeout(None)
        return sent

    def _recv(self, buffsize):
        correct_seq_numb = False
        print("-----chunks-----")
        print(buffsize)
        while not correct_seq_numb:
            pkt_received, source = self.socket.recvfrom(buffsize + self.SEQ_NUM_SIZE)
            seq_num_received, data_received = self.__unpack(pkt_received)

            print("pkt:")
            print(pkt_received)
            print("waiting:")
            print(self.receiver_seqnum)
            print("seq num received:")
            print(seq_num_received)
            if seq_num_received == self.receiver_seqnum:
                pkt = self.__pack(self.receiver_seqnum, b'')
                self.socket.sendto(pkt, source)
                self.receiver_seqnum = toggled(self.receiver_seqnum)
                correct_seq_numb = True
            else:
                pkt = self.__pack(toggled(self.receiver_seqnum), b'')
                self.socket.sendto(pkt, source)

        return data_received, source

    def recv(self, buffsize):
        print("quiero recibir estos bytes:")
        print(buffsize)
        data = []
        for i in range(0, buffsize, self.MAX_DATAGRAM_SIZE):
            print("-------Iteracion numero-------")
            print(i)
            d, s = self._recv(min(self.MAX_DATAGRAM_SIZE, buffsize - i))
            data.append(d)

        data = b''.join(data)
        print("received")
        print(data)
        return data, s
