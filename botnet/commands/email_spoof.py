from redmail import outlook
import time

from commands.command_base import CommandBase

# This sends a spoofed email using the Outlook email service 
class EmailSpoof(CommandBase):
    # Initializes three instance variables: 
    # username: the email address of the sender
    # password: the password for the sender email address
    # to_email: the email address of the recipient
    def __init__(self, username, password, to_email):
        self.username = username
        self.password = password
        self.to_email = to_email

    # Returns a string that contains the details of the email that was sent, including the subject, sender email address, recipient email address, and time sent.
    def get_details(self):
        return f"Email subject title: \'{self.subject}\'\nFrom: {self.username}\nTo: {self.to_email}\nAt: {self.time_sent}"


    # First retrieves the HTML email template and then
    # sends the spoofed email using the Outlook email service through redmail.
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

    # Retrieves an email template in spam_templates folder, sets the object's subject variable
    # returns the HTML as a string
    def get_email_template(self):
        with open('commands/spam_templates/teams_email.html', 'r', encoding='iso-8859-1') as f:
            html_string = f.read()
        self.subject = "Performance Check-up"
        return html_string