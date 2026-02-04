import aiosmtplib
from email.mime.text import MIMEText
from app.config import settings

async def send_email(to_email: str, subject: str, body: str):
    message = MIMEText(body)
    message["From"] = settings.email_from
    message["To"] = to_email
    message["Subject"] = subject

    await aiosmtplib.send(
        message,
        hostname=settings.email_host,
        port=settings.email_port,
        username=settings.email_username,
        password=settings.email_password,
        use_tls=True
    )
