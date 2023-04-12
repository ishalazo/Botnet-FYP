from redmail import outlook
import time

from commands.command_base import CommandBase

class EmailSpoof(CommandBase):
    def __init__(self, username, password, to_email):
        self.username = username
        self.password = password
        self.to_email = to_email

    def get_details(self):
        return f"Email subject title: \'{self.subject}\'\nFrom: {self.username}\nTo: {self.to_email}\nAt: {self.time_sent}"

    def execute(self): 
        outlook.username = self.username
        outlook.password = self.password
        html_temp = self.get_email_template()
        outlook.send(
            subject=self.subject,
            receivers=[self.to_email], 
            html=html_temp
        )
        self.time_sent = time.ctime(time.time())

    def get_email_template(self):
        with open('commands/spam_templates/teams_email.html', 'r', encoding='iso-8859-1') as f:
            html_string = f.read()
        self.subject = "Performance Check-up"
        return html_string