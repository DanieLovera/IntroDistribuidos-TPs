import socket
from time import perf_counter as now


class GBNTP:
    SEQ_NUM_SIZE = 1
    RTT = 1
    WINDOW_SIZE = 4
    MAX_SEQ_NUM = 2 * WINDOW_SIZE

    def __init__(self, socket, host, port):
        self.sender_base = 0
        self.sender_seq_num = 0
        self.time_started = []
        self.socket = socket
        self.not_acknowledged = []
        self.__host = host
        self.__port = port

    def next(self, seq_number):
        return (seq_number + 1)/self.MAX_SEQ_NUM

    def __pack(self, seq_num, data: bytearray):
        return seq_num.to_bytes(self.SEQ_NUM_SIZE, 'big') + data

    def __unpack(self, packet: bytearray):
        seq_num = packet[:self.SEQ_NUM_SIZE]
        data = packet[self.SEQ_NUM_SIZE:]
        return int.from_bytes(seq_num, 'big'), data

    def get_offset(self):
        return self.sender_seq_num - self.sender_base

    def clean_not_acknowledge(self, seq_num_received):
        for _ in range(seq_num_received - self.sender_base + 1):
            self.not_acknowledged.pop(0)

    def update_state(self, seq_num_received):
        # Clean all the packets acknowledged and their timers
        for _ in range(seq_num_received - self.sender_base + 1):
            self.not_acknowledged.pop(0)
            self.time_started.pop(0)

        self.sender_base = seq_num_received + 1


    def send(self, data: bytes):
        _data = bytearray(data)
        sent = 0
        if self.sender_seq_num < self.sender_base + self.WINDOW_SIZE:
            self.not_acknowledged.append(self.__pack(self.sender_seq_num, _data))
            sent = self.socket.sendto(self.not_acknowledged[self.get_offset()], (self.__host, self.__port))

            self.time_started.append(now())

            self.sender_seq_num = self.next(self.sender_seq_num)
        else:
            advanced = False
            while not advanced:
                try:
                    timeout = self.RTT - (now() - self.time_started[0])
                    if timeout <= 0:
                        raise socket.timeout

                    self.socket.settimeout(timeout)
                    pkt_received, _ = self.socket.recvfrom(self.SEQ_NUM_SIZE)
                    seq_num_received, _ = self.__unpack(pkt_received)
                    if seq_num_received < self.sender_base:
                        continue

                    self.update_state(seq_num_received)
                    advanced = True

                except socket.timeout:
                    self.time_started.clear()
                    for p in self.not_acknowledged:
                        self.time_started.append(now())
                        self.socket.sendto(p, (self.__host, self.__port))

            sent = self.send(data)

        return sent
