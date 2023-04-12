from socket import *
import sys
from threading import Thread

from commands.command_factory import command_factory

def receive():
    while True:
        msg = client_socket.recv(BUFSIZ).decode("utf8")
        if msg == "{quit}":
            client_socket.close()
            print(msg)
            break
        if "command=" in msg:
            execute_command(msg)
        if not msg:
            break
        
def send():
    while True:
        msg = input()
        client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            break

def send_details(msg):
    client_socket.send(bytes(msg, "utf8"))

# "command=do_something, param1=value1, param2=value2, param3=value3"
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

def execute_command(data):
    command_name, params = parse_command(data) 
    command = command_factory(command_name, params)
    command.execute()
    send_details(command.get_details())

HOST = sys.argv[1]
PORT = int(sys.argv[2])
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

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