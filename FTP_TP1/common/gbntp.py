# import socket
# from timer import Timer
# from time import perf_counter as now


# class GBNTP:
#     SEQ_NUM_SIZE = 1
#     WINDOW_SIZE = 4
#     MAX_SEQ_NUM = 2 * WINDOW_SIZE
#     MAX_DATAGRAM_SIZE = 20    # 64kb
#     MAX_TIMEOUTS = 4

#     def __init__(self, socket):
#         self.sender_base = 1
#         self.sender_seq_num = 1
#         self.not_acknowledged = []
#         self.socket = socket
#         self.receiver_seqnum = 1
#         self.timeout = Timer()

#     def next(self, seq_number):
#         return (seq_number + 1)%self.MAX_SEQ_NUM

#     def prev(self, seq_number):
#         return (seq_number - 1)%self.MAX_SEQ_NUM

#     def __pack(self, seq_num, data: bytearray):
#         return seq_num.to_bytes(self.SEQ_NUM_SIZE, 'big') + data

#     def __unpack(self, packet: bytearray):
#         seq_num = packet[:self.SEQ_NUM_SIZE]
#         data = packet[self.SEQ_NUM_SIZE:]
#         return int.from_bytes(seq_num, 'big'), data

#     def get_offset(self):
#         return (self.sender_seq_num - self.sender_base)%self.MAX_SEQ_NUM

#     def update_state(self, seq_num_received, start):
#         # Clean all the packets acknowledged and their timers
#         self.timeout.calculateTimeout(now() - start)

#         for _ in range((seq_num_received - self.sender_base + 1)%self.MAX_SEQ_NUM):
#             self.not_acknowledged.pop(0)

#         self.sender_base = (seq_num_received + 1)%self.MAX_SEQ_NUM

#     def send_in_window(self):
#         # When the window cover the end and the beginning of the sequence numbers
#         if self.sender_base + self.WINDOW_SIZE >= self.MAX_SEQ_NUM and self.sender_seq_num < self.WINDOW_SIZE:
#             return self.sender_seq_num < (self.sender_base + self.WINDOW_SIZE)%self.MAX_SEQ_NUM

#         return self.sender_seq_num < self.sender_base + self.WINDOW_SIZE

#     def _send_a_packet(self, data: bytearray, host, port, last_send: bool):
#         sent = 0
#         print("Envio un pedazo:")
#         print(data)
#         start = 0
#         if self.send_in_window():
#             print("numero de sequencia enviando")
#             print(self.sender_seq_num)
#             self.not_acknowledged.append(
#                 self.__pack(self.sender_seq_num, data)
#             )
#             sent = self.socket.sendto(
#                 self.not_acknowledged[self.get_offset()], (host, port)
#             )
#             if self.sender_seq_num == self.sender_base:
#                 start = now()

#             self.sender_seq_num = self.next(self.sender_seq_num)
#         else:
#             advanced = False
#             while not advanced:
#                 try:
#                     timeout = self.timeout.getTimeout() - (now() - start)
#                     if timeout <= 0:
#                         raise socket.timeout

#                     self.socket.settimeout(timeout)
#                     pkt_received, _ = self.socket.recvfrom(self.SEQ_NUM_SIZE)
#                     seq_num_received, _ = self.__unpack(pkt_received)
#                     print("numero de secuencia recivido")
#                     print(seq_num_received)
#                     print("base actual")
#                     print(self.sender_base)
#                     # Border cases: partial window at the end
#                     # and at the beginning
#                     if self.sender_base + self.WINDOW_SIZE >= \
#                             self.MAX_SEQ_NUM and seq_num_received < \
#                                 self.sender_base and seq_num_received > \
#                                     (self.sender_base + self.WINDOW_SIZE) \
#                                         % self.MAX_SEQ_NUM:
#                         continue
#                     elif self.sender_base + self.WINDOW_SIZE < \
#                             self.MAX_SEQ_NUM and (seq_num_received <
#                                 self.sender_base or seq_num_received >
#                                     self.sender_base + self.WINDOW_SIZE):
#                         continue

#                     self.update_state(seq_num_received, start)
#                     start = now()
#                     advanced = True

#                 except socket.timeout:
#                     self.timeout.timeout()
#                     start = now()
#                     for p in self.not_acknowledged:
#                         self.socket.sendto(p, (host, port))

#             sent = self._send_a_packet(data, host, port, last_send)

#         # Ensure all the data had been sent to destination
#         # because there won't be more send
#         if last_send:
#             print("-----------Ultimo envio-----------")
#             timeouts = 0
#             while not len(self.not_acknowledged) == 0:
#                 print("tamaño")
#                 print(len(self.not_acknowledged))
#                 try:
#                     timeout = self.timeout.getTimeout() - (now() - start)
#                     if timeout <= 0:
#                         raise socket.timeout

#                     self.socket.settimeout(timeout)
#                     pkt_received, _ = self.socket.recvfrom(self.SEQ_NUM_SIZE)
#                     seq_num_received, _ = self.__unpack(pkt_received)
#                     print("numero de secuencia recivido")
#                     print(seq_num_received)
#                     print("base actual")
#                     print(self.sender_base)
#                     if self.sender_base + self.WINDOW_SIZE >= \
#                             self.MAX_SEQ_NUM and seq_num_received < \
#                                 self.sender_base and seq_num_received > \
#                                     (self.sender_base + self.WINDOW_SIZE) \
#                                         % self.MAX_SEQ_NUM:
#                         timeouts = 0
#                         continue
#                     elif self.sender_base + self.WINDOW_SIZE < \
#                             self.MAX_SEQ_NUM and (seq_num_received <
#                                 self.sender_base or seq_num_received >
#                                     self.sender_base + self.WINDOW_SIZE):
#                         timeouts = 0
#                         continue

#                     self.update_state(seq_num_received, start)
#                     start = now()
#                 except socket.timeout:
#                     self.timeout.timeout()
#                     print("Reenviando paquetes")
#                     start = now()
#                     if last_send:
#                         timeouts += 1
#                     for p in self.not_acknowledged:
#                         print("Reenviando paquet")
#                         print(p)
#                         self.socket.sendto(p, (host, port))

#                 # If the last ack is lost
#                 if timeouts >= self.MAX_TIMEOUTS:
#                     break

#         return sent

#     def send(self, data: bytes, host, port):
#         print("Quiero enviar")
#         print(data)
#         _data = bytearray(data)
#         sent = 0

#         for i in range(0, len(_data), self.MAX_DATAGRAM_SIZE):
#             last_send = False

#             if i + self.MAX_DATAGRAM_SIZE > len(_data):
#                 print("Ultimo pedazo")
#                 last_send = True

#             sent += self._send_a_packet(
#                 _data[i:min(i + self.MAX_DATAGRAM_SIZE, len(_data))],
#                 host,
#                 port,
#                 last_send
#             )

#         self.socket.settimeout(None)
#         return sent

#     def _recv(self, buffsize):
#         print("quiero recibir en pedazo estos bytes:")
#         print(buffsize)
#         correct_seq_numb = False
#         while not correct_seq_numb:
#             pkt_received, source = self.socket.recvfrom(buffsize + self.SEQ_NUM_SIZE)
#             seq_num_received, data_received = self.__unpack(pkt_received)

#             print("numero de sequencia recibido")
#             print(seq_num_received)
#             print("numero de sequencia esperado")
#             print(self.receiver_seqnum)

#             if seq_num_received == self.receiver_seqnum:
#                 pkt = self.__pack(self.receiver_seqnum, b'')
#                 self.socket.sendto(pkt, source)
#                 self.receiver_seqnum = self.next(self.receiver_seqnum)
#                 correct_seq_numb = True
#             else:
#                 print("Reenviando el ack")
#                 print(self.prev(self.receiver_seqnum))
#                 pkt = self.__pack(self.prev(self.receiver_seqnum), b'')
#                 self.socket.sendto(pkt, source)

#         return data_received, source

#     def recv(self, buffsize):
#         print("quiero recibir estos bytes:")
#         print(buffsize)
#         received = 0
#         data = []
#         for i in range(0, buffsize, self.MAX_DATAGRAM_SIZE):
#             print("-------Iteracion numero-------")
#             print(i)
#             d, s = self._recv(min(self.MAX_DATAGRAM_SIZE, buffsize - i))
#             print("data")
#             print(d)
#             data.append(d)
#             received += len(d)

#         data = b''.join(data)
#         print("received")
#         print(data)
#         return data, s

import socket
from timer import Timer
from time import perf_counter as now


class GBNTP:
    DATA_SIZE = 1
    SEQ_NUM_SIZE = 1
    WINDOW_SIZE = 4
    MAX_SEQ_NUM = 2 * WINDOW_SIZE
    MAX_DATAGRAM_SIZE = 20    # 64kb
    MAX_TIMEOUTS = 4
    TYPE_DATA = b'd'
    TYPE_ACK = b'a'

    def __init__(self, socket):
        self.sender_base = 1
        self.sender_seq_num = 1
        self.not_acknowledged = []
        self.socket = socket
        self.receiver_seqnum = 1
        self.timeout = Timer()

    def next(self, seq_number):
        return (seq_number + 1)%self.MAX_SEQ_NUM

    def prev(self, seq_number):
        return (seq_number - 1)%self.MAX_SEQ_NUM

    def __pack(self, seq_num, type_data, data: bytearray):
        return seq_num.to_bytes(self.SEQ_NUM_SIZE, 'big') + type_data + data

    def __unpack(self, packet: bytearray):
        seq_num = packet[:self.SEQ_NUM_SIZE]
        type_data = packet[
            self.SEQ_NUM_SIZE:self.SEQ_NUM_SIZE + self.DATA_SIZE
        ]
        data = packet[self.SEQ_NUM_SIZE + self.DATA_SIZE:]
        return int.from_bytes(seq_num, 'big'), type_data, data

    def get_offset(self):
        return (self.sender_seq_num - self.sender_base)%self.MAX_SEQ_NUM

    def update_state(self, seq_num_received, start):
        # Clean all the packets acknowledged and their timers
        self.timeout.calculateTimeout(now() - start)

        for _ in range((seq_num_received - self.sender_base + 1)%self.MAX_SEQ_NUM):
            self.not_acknowledged.pop(0)

        self.sender_base = (seq_num_received + 1)%self.MAX_SEQ_NUM

    def send_in_window(self):
        # When the window cover the end and the beginning of the sequence numbers
        if self.sender_base + self.WINDOW_SIZE >= self.MAX_SEQ_NUM and self.sender_seq_num < self.WINDOW_SIZE:
            return self.sender_seq_num < (self.sender_base + self.WINDOW_SIZE)%self.MAX_SEQ_NUM

        return self.sender_seq_num < self.sender_base + self.WINDOW_SIZE

    def _send_a_packet(self, data: bytearray, host, port, last_send: bool):
        sent = 0
        print("Envio un pedazo:")
        print(data)
        start = 0
        if self.send_in_window():
            print("numero de sequencia enviando")
            print(self.sender_seq_num)
            self.not_acknowledged.append(
                self.__pack(self.sender_seq_num, self.TYPE_DATA, data)
            )
            sent = self.socket.sendto(
                self.not_acknowledged[self.get_offset()], (host, port)
            )
            if self.sender_seq_num == self.sender_base:
                start = now()

            self.sender_seq_num = self.next(self.sender_seq_num)
        else:
            advanced = False
            while not advanced:
                try:
                    timeout = self.timeout.getTimeout() - (now() - start)
                    if timeout <= 0:
                        raise socket.timeout

                    self.socket.settimeout(timeout)
                    pkt_received, _ = self.socket.recvfrom(self.SEQ_NUM_SIZE + self.DATA_SIZE)
                    seq_num_received, type_data, _ = self.__unpack(pkt_received)
                    print("numero de secuencia recivido")
                    print(seq_num_received)
                    print("base actual")
                    print(self.sender_base)

                    # We expect only acks
                    if type_data == self.TYPE_DATA:
                        continue

                    # Border cases: partial window at the end
                    # and at the beginning
                    if self.sender_base + self.WINDOW_SIZE >= \
                            self.MAX_SEQ_NUM and seq_num_received < \
                                self.sender_base and seq_num_received > \
                                    (self.sender_base + self.WINDOW_SIZE) \
                                        % self.MAX_SEQ_NUM:
                        continue
                    elif self.sender_base + self.WINDOW_SIZE < \
                            self.MAX_SEQ_NUM and (seq_num_received <
                                self.sender_base or seq_num_received >
                                    self.sender_base + self.WINDOW_SIZE):
                        continue

                    self.update_state(seq_num_received, start)
                    start = now()
                    advanced = True

                except socket.timeout:
                    self.timeout.timeout()
                    start = now()
                    for p in self.not_acknowledged:
                        self.socket.sendto(p, (host, port))

            sent = self._send_a_packet(data, host, port, last_send)

        # Ensure all the data had been sent to destination
        # because there won't be more send
        if last_send:
            print("-----------Ultimo envio-----------")
            timeouts = 0
            while not len(self.not_acknowledged) == 0:
                print("tamaño")
                print(len(self.not_acknowledged))
                try:
                    timeout = self.timeout.getTimeout() - (now() - start)
                    if timeout <= 0:
                        raise socket.timeout

                    self.socket.settimeout(timeout)
                    pkt_received, _ = self.socket.recvfrom(self.SEQ_NUM_SIZE + self.DATA_SIZE)
                    seq_num_received, type_data, _ = self.__unpack(pkt_received)
                    print("numero de secuencia recivido")
                    print(seq_num_received)
                    print("base actual")
                    print(self.sender_base)
                    # We expect only acks
                    if type_data == self.TYPE_DATA:
                        continue

                    if self.sender_base + self.WINDOW_SIZE >= \
                            self.MAX_SEQ_NUM and seq_num_received < \
                                self.sender_base and seq_num_received > \
                                    (self.sender_base + self.WINDOW_SIZE) \
                                        % self.MAX_SEQ_NUM:
                        timeouts = 0
                        continue
                    elif self.sender_base + self.WINDOW_SIZE < \
                            self.MAX_SEQ_NUM and (seq_num_received <
                                self.sender_base or seq_num_received >
                                    self.sender_base + self.WINDOW_SIZE):
                        timeouts = 0
                        continue

                    self.update_state(seq_num_received, start)
                    start = now()
                except socket.timeout:
                    self.timeout.timeout()
                    print("Reenviando paquetes")
                    start = now()
                    if last_send:
                        timeouts += 1
                    for p in self.not_acknowledged:
                        print("Reenviando paquet")
                        print(p)
                        self.socket.sendto(p, (host, port))

                # If the last ack is lost
                if timeouts >= self.MAX_TIMEOUTS:
                    break

        return sent

    def send(self, data: bytes, host, port):
        print("Quiero enviar")
        print(data)
        _data = bytearray(data)
        sent = 0

        for i in range(0, len(_data), self.MAX_DATAGRAM_SIZE):
            last_send = False

            if i + self.MAX_DATAGRAM_SIZE > len(_data):
                print("Ultimo pedazo")
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
        print("quiero recibir en pedazo estos bytes:")
        print(buffsize)
        correct_seq_numb = False
        while not correct_seq_numb:
            pkt_received, source = self.socket.recvfrom(buffsize + self.DATA_SIZE + self.SEQ_NUM_SIZE)
            seq_num_received, type_data, data_received = self.__unpack(pkt_received)

            print("numero de sequencia recibido")
            print(seq_num_received)
            print("numero de sequencia esperado")
            print(self.receiver_seqnum)

            # We expect only data
            if type_data == self.TYPE_ACK:
                continue

            if seq_num_received == self.receiver_seqnum:
                pkt = self.__pack(self.receiver_seqnum, self.TYPE_ACK, b'')
                self.socket.sendto(pkt, source)
                self.receiver_seqnum = self.next(self.receiver_seqnum)
                correct_seq_numb = True
            else:
                print("Reenviando el ack")
                print(self.prev(self.receiver_seqnum))
                pkt = self.__pack(self.prev(self.receiver_seqnum), self.TYPE_ACK, b'')
                self.socket.sendto(pkt, source)

        return data_received, source

    def recv(self, buffsize):
        print("quiero recibir estos bytes:")
        print(buffsize)
        received = 0
        data = []
        for i in range(0, buffsize, self.MAX_DATAGRAM_SIZE):
            print("-------Iteracion numero-------")
            print(i)
            d, s = self._recv(min(self.MAX_DATAGRAM_SIZE, buffsize - i))
            print("data")
            print(d)
            data.append(d)
            received += len(d)

        data = b''.join(data)
        print("received")
        print(data)
        return data, s
