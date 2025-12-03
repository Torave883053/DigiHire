import smtplib
from email.mime.text import MIMEText

SENDER_EMAIL = "toravepravin@gmail.com"
SENDER_PASSWORD = "jhka novs metv ccyi"   # App Password

def send_vendor_email(
    to_email: str,
    username: str,
    password: str,
    login_url: str,
    vendor_name: str
):

    subject = "DigiHire | Your Vendor Account Login Details"

    body = f"""
Hello {vendor_name},

Welcome to DigiHire!

Your vendor account has been successfully created.
Please find your login credentials below:

----------------------------------------
🔐 Login Credentials
• Login URL : {login_url}
• Username  : {username}
• Password  : {password}
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

    # 🚀 Send email directly, no background task
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
