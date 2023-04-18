import time
import urllib.request
import socket
import netifaces as ni

from commands.command_base import CommandBase 

# Retrieves certain data about a client/bot
class Status(CommandBase):

    def execute(self):
        # find host name
        self.hostname = socket.gethostname()

        # find ip address
        # for windows: 
        # self.ip = socket.gethostbyname(self.hostname)
        # for linux:
        self.ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']

        # Rest internet reachability
        self.internet_access = False
        try:
            urllib.request.urlopen('http://google.com')
            self.internet_access = True
        except:
            pass

        self.timestamp = time.ctime(time.time())
    
    # Returns the details found as a string
    def get_details(self):
        return f"Hostname: {self.hostname}\nIP: {self.ip}\nInternet Access: {self.internet_access}\nStatus checked at \n{self.timestamp}"