# import socket   
# hostname=socket.gethostname()   
# IPAddr=socket.gethostbyname(hostname)   
# print("Your Computer Name is:"+hostname)   
# print("Your Computer IP Address is:"+IPAddr)  

# import netifaces as ni
# ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
# print(ip)

# Import smtplib for the actual sending function
# from email.mime.multipart import MIMEMultipart
# import smtplib

# # Import the email modules we'll need
# from email.mime.text import MIMEText

# # Open a plain text file for reading.  For this example, assume that
# # the text file contains only ASCII characters.

# msg = MIMEMultipart()
# me = "terry.kichirou@gmail.com"
# you = "wirav24020@dogemn.com"
# msg['Subject'] = "Fuck you"
# msg['From'] = me
# msg['To'] = you
# body = "Dear Recipient,\n\nI am writing to share some important information about defeating scams.\n\nSincerely,\nYour Name"

# msg.attach(MIMEText(body, "plain"))

# # Send the message via our own SMTP server, but don't include the
# # envelope header.
# s = smtplib.SMTP('localhost')
# s.sendmail(me, [you], msg.as_string())
# s.quit()

from redmail import outlook
outlook.username = 'terry.kichirou@outlook.com'
outlook.password = 'VtmVbnS3'

with open('commands/teams_email.html', 'r', encoding='utf-8') as f:
    html_string = f.read()

# And then you can send emails
outlook.send(
    subject="Together we can defeat scams",
    receivers=['wirav24020@dogemn.com'], 
    html=html_string
)