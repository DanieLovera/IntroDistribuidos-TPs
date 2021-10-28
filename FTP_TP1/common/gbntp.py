import socket
from time import perf_counter as now


class GBNTP:
    SEQ_NUM_SIZE = 1
    RTT = 1
    WINDOW_SIZE = 4
    MAX_SEQ_NUM = 2 * WINDOW_SIZE
    MAX_DATAGRAM_SIZE = 64000    # 64kb

    def __init__(self, socket):
        self.sender_base = 1
        self.sender_seq_num = 1
        self.time_started = []
        self.not_acknowledged = []
        self.socket = socket
        self.receiver_seqnum = 1

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

    def update_state(self, seq_num_received):
        # Clean all the packets acknowledged and their timers
        for _ in range((seq_num_received - self.sender_base + 1)%self.MAX_SEQ_NUM):
            self.not_acknowledged.pop(0)
            self.time_started.pop(0)

        self.sender_base = (seq_num_received + 1)%self.MAX_SEQ_NUM

    def send_in_window(self):
        # When the window cover the end and the beginning of the sequence numbers
        if self.sender_base + self.WINDOW_SIZE >= self.MAX_SEQ_NUM and self.sender_seq_num < self.WINDOW_SIZE:
            return self.sender_seq_num < (self.sender_base + self.WINDOW_SIZE)%self.MAX_SEQ_NUM

        return self.sender_seq_num < self.sender_base + self.WINDOW_SIZE

    def _send_a_packet(self, data: bytearray, host, port, last_send: bool):
        sent = 0
        # print("Envio un pedazo:")
        # print(data)

        if self.send_in_window():
            # print("numero de sequencia enviando")
            # print(self.sender_seq_num)
            self.not_acknowledged.append(
                self.__pack(self.sender_seq_num, data)
            )
            sent = self.socket.sendto(
                self.not_acknowledged[self.get_offset()], (host, port)
            )
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
                    # print("numero de secuencia recivido")
                    # print(seq_num_received)
                    if seq_num_received < self.sender_base:
                        continue

                    self.update_state(seq_num_received)
                    advanced = True

                except socket.timeout:
                    self.time_started.clear()
                    for p in self.not_acknowledged:
                        self.time_started.append(now())
                        self.socket.sendto(p, (host, port))

            sent = self.send(data, host, port, last_send)

        # Ensure all the data had been sent to destination
        # because there won't be more send
        if last_send:
            # print("-----------Ultimo envio-----------")
            while not len(self.not_acknowledged) == 0:
                # print("tamaño")
                # print(len(self.not_acknowledged))
                try:
                    timeout = self.RTT - (now() - self.time_started[0])
                    if timeout <= 0:
                        raise socket.timeout

                    self.socket.settimeout(timeout)
                    pkt_received, _ = self.socket.recvfrom(self.SEQ_NUM_SIZE)
                    seq_num_received, _ = self.__unpack(pkt_received)
                    # print("numero de secuencia recivido")
                    # print(seq_num_received)
                    if seq_num_received < self.sender_base:
                        continue

                    self.update_state(seq_num_received)
                except socket.timeout:
                    # print("Reenviando paquetes")
                    self.time_started.clear()
                    for p in self.not_acknowledged:
                        # print("Reenviando paquet")
                        # print(p)
                        self.time_started.append(now())
                        self.socket.sendto(p, (host, port))

        return sent

    def send(self, data: bytes, host, port):
        # print("Quiero enviar")
        # print(data)
        _data = bytearray(data)
        sent = 0

        for i in range(0, len(_data), self.MAX_DATAGRAM_SIZE):
            last_send = False

            if i + self.MAX_DATAGRAM_SIZE > len(_data):
                # print("Ultimo pedazo")
                last_send = True

            sent += self._send_a_packet(
                _data[i:min(i + self.MAX_DATAGRAM_SIZE, len(_data))],
                host,
                port,
                last_send
            )

        return sent

    def _recv(self, buffsize):
        # print("quiero recibir en pedazo estos bytes:")
        # print(buffsize)
        correct_seq_numb = False
        while not correct_seq_numb:
            pkt_received, source = self.socket.recvfrom(buffsize + self.SEQ_NUM_SIZE)
            seq_num_received, data_received = self.__unpack(pkt_received)

            # print("numero de sequencia recibido")
            # print(seq_num_received)
            # print("numero de sequencia esperado")
            # print(self.receiver_seqnum)

            if seq_num_received == self.receiver_seqnum and len(data_received) == buffsize:
                pkt = self.__pack(self.receiver_seqnum, b'')
                self.socket.sendto(pkt, source)
                self.receiver_seqnum = self.next(self.receiver_seqnum)
                correct_seq_numb = True
            else:
                # print("Reenviando el ack")
                # print(self.prev(self.receiver_seqnum))
                pkt = self.__pack(self.prev(self.receiver_seqnum), b'')
                self.socket.sendto(pkt, source)

        return data_received, source

    def recv(self, buffsize):
        # print("quiero recibir estos bytes:")
        # print(buffsize)
        received = 0
        data = []
        for i in range(0, buffsize, self.MAX_DATAGRAM_SIZE):
            # print("-------Iteracion numero-------")
            # print(i)
            d, s = self._recv(min(self.MAX_DATAGRAM_SIZE, buffsize - i))
            # print("data")
            # print(d)
            data.append(d)
            received += len(d)

        data = b''.join(data)
        # print("received")
        # print(data)
        return data, s
