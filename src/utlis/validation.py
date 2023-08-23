import logging
import smtplib

from src.utlis.mail import login_smtp
from src.utlis.mysql_client import run_server_check, run_database_check


def database_validation():
    run_server_check()
    run_database_check()


def smtp_validation():
    try:
        login_smtp()
    except smtplib.SMTPException as e:
        logging.error("SMTP Validation Error: " + str(e))
        exit(0)
    except Exception as e:
        logging.error("SMTP Validation Error: " + str(e))
        exit(0)
