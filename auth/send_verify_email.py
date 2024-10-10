import aiosmtplib
import os
import sys

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '../'))
sys.path.append(root_dir)

from config import sender_email, email_app_password

async def send_email(receiver_email: str, token: str):

    subject = "Verify token"
    body = f"Your verify token: {token}"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    smtp_host = "smtp.gmail.com"
    smtp_port = 587
    username = sender_email
    password = email_app_password

    await aiosmtplib.send(
        message,
        hostname=smtp_host,
        port=smtp_port,
        start_tls=True,
        username=username,
        password=password,
    )