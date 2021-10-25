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
        self.receiver_seqnum = 0
        self.__host = host
        self.__port = port

    def next(self, seq_number):
        return (seq_number + 1)%self.MAX_SEQ_NUM

    def prev(self, seq_number):
        return (seq_number - 1)%self.MAX_SEQ_NUM

    def __pack(self, seq_num, data: bytearray):
        return seq_num.to_bytes(self.SEQ_NUM_SIZE, 'big') + data

    def __unpack(self, packet: bytearray):
        seq_num = packet[:self.SEQ_NUM_SIZE]
        data = packet[self.SEQ_NUM_SIZE:]
        return int.from_bytes(seq_num, 'big'), data

    def get_offset(self):
        return (self.sender_seq_num - self.sender_base)%self.MAX_SEQ_NUM

    def clean_not_acknowledge(self, seq_num_received):
        for _ in range((seq_num_received - self.sender_base + 1)):
            self.not_acknowledged.pop(0)

    def update_state(self, seq_num_received):
        # Clean all the packets acknowledged and their timers
        for _ in range((seq_num_received - self.sender_base + 1)):
            self.not_acknowledged.pop(0)
            self.time_started.pop(0)

        self.sender_base = (seq_num_received + 1)%self.MAX_SEQ_NUM

    def send_in_window(self):
        # When the window cover the end and the beginning of the sequence numbers
        if self.sender_base + self.WINDOW_SIZE >= self.MAX_SEQ_NUM and self.sender_seq_num < self.WINDOW_SIZE:
            return self.sender_seq_num < (self.sender_base + self.WINDOW_SIZE)%self.MAX_SEQ_NUM

        return self.sender_seq_num < self.sender_base + self.WINDOW_SIZE

    def send(self, data: bytes):
        print("---------SEND START--------")
        _data = bytearray(data)
        sent = 0
        print("seq_number")
        print(self.sender_seq_num)

        print("base")
        print(self.sender_base)
        if self.send_in_window():
            self.not_acknowledged.append(self.__pack(self.sender_seq_num, _data))
            if len(self.not_acknowledged) > 4:
                self.not_acknowledged[20]

            sent = self.socket.sendto(self.not_acknowledged[self.get_offset()], (self.__host, self.__port))

            self.time_started.append(now())

            print("timers")
            print(self.time_started)

            self.sender_seq_num = self.next(self.sender_seq_num)
        else:
            print("---------WINDOW FULL--------")
            advanced = False
            while not advanced:
                try:
                    timeout = self.RTT - (now() - self.time_started[0])
                    if timeout <= 0:
                        print("timeout a mano")
                        print(timeout)
                        raise socket.timeout

                    self.socket.settimeout(timeout)
                    pkt_received, _ = self.socket.recvfrom(self.SEQ_NUM_SIZE)
                    seq_num_received, _ = self.__unpack(pkt_received)
                    if seq_num_received < self.sender_base:
                        print("Incorrect seq_num_received")
                        print(seq_num_received)
                        continue

                    print("Correct seq_num_received")
                    print(seq_num_received)
                    self.update_state(seq_num_received)
                    advanced = True

                except socket.timeout:
                    print("timeout excepcion")
                    self.time_started.clear()
                    for p in self.not_acknowledged:
                        self.time_started.append(now())
                        self.socket.sendto(p, (self.__host, self.__port))

            sent = self.send(data)

        return sent

    def recv(self, buffsize):
        print("---------RECV START--------")
        correct_seq_numb = False
        while not correct_seq_numb:
            pkt_received, source = self.socket.recvfrom(buffsize + self.SEQ_NUM_SIZE)
            seq_num_received, data_received = self.__unpack(pkt_received)
            print("data received")
            print(data_received)

            if seq_num_received == self.receiver_seqnum:
                print("Seq_num_expected")
                print(seq_num_received)
                pkt = self.__pack(self.receiver_seqnum, b'')
                self.socket.sendto(pkt, source)
                self.receiver_seqnum = self.next(self.receiver_seqnum)
                correct_seq_numb = True
            else:
                print("incorrect seq_num_expected")
                print(seq_num_received)
                pkt = self.__pack(self.prev(self.receiver_seqnum), b'')
                self.socket.sendto(pkt, source)

        return data_received
