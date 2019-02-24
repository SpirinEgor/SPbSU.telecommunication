import socket
import time
import struct
import random

class SNTP():

    NTP_SERVERS = [
        '0.ru.pool.ntp.org',
        '1.ru.pool.ntp.org',
        '2.ru.pool.ntp.org',
        '3.ru.pool.ntp.org'
    ]
    PORT = 123
    TIME_ZERO = 2208988800

    def __init__(self):
        self.ntp_server = random.choice(self.NTP_SERVERS)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.delays = []
        self.local_shifts = []

    def request(self):
        data = '\x1b' + 47 * '\0'
        t1 = time.time()
        self.client.sendto(data.encode('utf-8'), (self.ntp_server, self.PORT))
        data, _ = self.client.recvfrom(1024)
        t4 = time.time()
        assert data, 'ntp server doesn\' return data'
        data_decoded = struct.unpack('!12I', data)
        t2 = data_decoded[8] + float('0.' + str(data_decoded[9])) - self.TIME_ZERO
        t3 = data_decoded[10] + float('0.' + str(data_decoded[11])) - self.TIME_ZERO
        return t1, t2, t3, t4

    def calc_shifts_delays(self, n):
        for _ in range(n):
            t1, t2, t3, t4 = self.request()
            self.delays.append((t2 - t1) + (t4 - t3))
            self.local_shifts.append(((t2 - t1) + (t3 - t4)) / 2)

    def print_statistic(self):
        assert len(self.delays) and len(self.local_shifts),\
               'run calculation before collecting statistic'
        size = len(self.delays)
        mean_delay = sum(self.delays) / size
        mean_local_shift = sum(self.local_shifts) / size
        print(f'use {self.ntp_server} {size} times')
        print(f'mean delay: {mean_delay}')
        print(f'mean local shift: {mean_local_shift}')


if __name__ == '__main__':
    sntp = SNTP()
    sntp.calc_shifts_delays(5)
    sntp.print_statistic()