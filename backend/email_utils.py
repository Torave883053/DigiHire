# email_utils.py
import smtplib
from email.mime.text import MIMEText
from fastapi import BackgroundTasks

SENDER_EMAIL = "toravepravin@gmail.com"
SENDER_PASSWORD = "jhka novs metv ccyi"

def send_reset_email(background_tasks: BackgroundTasks, to_email: str, Username: str,Password: str):
    subject = "Welcome to DigiHire - Username and Password Information"
    body = f"""
    Hello,

    Below are your Username and Password to access DigiHire:
    Username :- {Username}
    Password :- {Password}

    Regards,
    DigiHire Team
    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email

    def send_mail():
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

    background_tasks.add_task(send_mail)
