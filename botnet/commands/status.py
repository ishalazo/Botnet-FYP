import time
import urllib.request
import socket
import netifaces as ni

from commands.command_base import CommandBase 

class Status(CommandBase):

# TODO: MAKE THE EXECUTE SEND A MESSAGE TO SERVER?
    def execute(self):
        self.get_hostname_ip()
        self.internet_reachability()
        status = f"Hostname={self.hostname}, IP={self.ip}, Internet Access={self.internet_access}"
        self.timestamp = time.ctime(time.time())
        return status
    
    def get_metrics(self):
        return f"Status checked at {self.timestamp}"

    def get_hostname_ip(self):
        self.hostname = socket.gethostname()   
        # for windows: 
        # self.ip = socket.gethostbyname(self.hostname)
        # for linux:
        self.ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
        return self.hostname, self.ip
    
    def internet_reachability(self, host='http://google.com'):
        self.internet_access = False
        try:
            urllib.request.urlopen(host)
            self.internet_access = True
        except:
            pass
        return self.internet_access

if __name__ == "__main__":
    status_cmd = Status('status')

    hostname, ip = status_cmd.get_hostname_ip()
    print(f'Hostname: {hostname}, IP Address: {ip}')

    internet_access = status_cmd.internet_reachability()
    print(f'Internet Access: {internet_access}')

    status = status_cmd.execute()
    print(status)

    metrics = status_cmd.get_metrics()
    print(metrics)