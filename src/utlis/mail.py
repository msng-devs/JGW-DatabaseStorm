import yaml
import smtplib
from email.message import EmailMessage

from src.utlis.config import load_config

conf = load_config()


def login_smtp():
    smtp = smtplib.SMTP_SSL(conf["SMTP_SERVER"], conf["SMTP_PORT"])
    smtp.login(conf["SMTP_USER"], conf["SMTP_PASSWORD"])
    return smtp


def send_mail(subject: str, text: str):
    smtp = login_smtp()

    message = EmailMessage()

    message["Subject"] = subject
    message.set_content(text)
    message["From"] = conf["SMTP_FROM"]
    message["To"] = conf["SMTP_TO"]

    smtp.send_message(message)
    smtp.quit()
