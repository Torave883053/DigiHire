# email_utils.py

import smtplib
from email.mime.text import MIMEText
from fastapi import BackgroundTasks

SENDER_EMAIL = "toravepravin@gmail.com"
SENDER_PASSWORD = "jhka novs metv ccyi"   # App Password


def send_reset_email(
    background_tasks: BackgroundTasks,
    to_email: str,
    Username: str,
    Password: str,
    LoginURL: str,
    VendorName: str
):
    subject = "DigiHire | Your Vendor Account Login Details"

    body = f"""
Hello {VendorName},

Welcome to DigiHire!

Your vendor account has been successfully created.
Please find your login credentials below:

----------------------------------------
🔐 Login Credentials
• Login URL : {LoginURL}
• Username  : {Username}
• Password  : {Password}
----------------------------------------

You can now log in and access your vendor dashboard.

If you have any questions or need any assistance,
please feel free to reach out to our support team.

Best Regards,
DigiHire Team
www.digihire.com
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
