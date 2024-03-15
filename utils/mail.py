import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def create_email(subject, body, from_addr, to_addr):
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    return msg.as_string()


def send_email(email_content, from_addr, to_addr, password):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr, email_content)
    server.quit()


# use the csv to get the recitpentis
recipients = ['example1@example.com', 'example2@example.com']

# Sender's email address and password
from_addr = 'your-email@gmail.com'
password = 'your-password'

# Email subject and body
subject = 'Your Subject Here'
body = 'Your email body here.'

# Loop through recipients and send emails
for to_addr in recipients:
    email_content = create_email(subject, body, from_addr, to_addr)
    send_email(email_content, from_addr, to_addr, password)

