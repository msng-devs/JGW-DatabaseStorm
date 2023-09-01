import logging

import yaml
import smtplib
from email.message import EmailMessage
import json
import zmq
from src.utlis.config import load_config

config = load_config()


def send_mail(subject: str, text: str):
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUSH)
    zmq_socket.bind(f"tcp://{config.mailstorm_server}:{config.mailstorm_port}")

    message = {
        "to": f"{config.mailstorm_to}",
        "subject": subject,
        "template": "database-storm",
        "arg": {
            "content": text,
        },
        "who": "databaseStorm"
    }
    request = json.dumps(message, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False)
    zmq_socket.send_json(request)
    logging.info("Send Mail to MailStorm Server.")
