from redmail import outlook
import time

from commands.command_base import CommandBase

class EmailSpoof(CommandBase):
    def __init__(self, username, password, to_email):
        self.username = username
        self.password = password
        self.to_email = to_email

    def get_metrics(self):
        return f"Email sent at {self.time_sent}"

    def execute(self): 
        outlook.username = self.username
        outlook.password = self.password
        html_temp, subject = self.get_email_template()
        outlook.send(
            subject=subject,
            receivers=[self.to_email], 
            html=html_temp
        )
        self.time_sent = time.ctime(time.time())

    def get_email_template(self):
        with open('commands/spam_templates/teams_email.html', 'r', encoding='iso-8859-1') as f:
            html_string = f.read()
        subject = "Performance Check-up"
        return html_string, subject
    
if __name__ == "__main__":
    email = EmailSpoof('terry.kichirou@outlook.com','VtmVbnS3','wirav24020@dogemn.com')
    email.execute()
    print(email.get_metrics())