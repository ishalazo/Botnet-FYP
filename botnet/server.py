import socket 

class Server:
    def __init__(self, ip, port):
        self._ip = ip
        self._port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self._ip, self._port))
        self.socket.listen(10)
        self._client_socket, self._client_address = self.socket.accept()

    def receive(self):
        data = self._client_socket.recv(1024)
        return data.decode()

    def send(self, message):
        self._client_socket.sendall(message.encode())

    def close(self):
        self._client_socket.close()
        self.socket.close()
