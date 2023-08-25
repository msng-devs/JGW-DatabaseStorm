import logging
import smtplib
from datetime import datetime

from src.utlis.mail import send_mail
from src.utlis.mysql_client import run_server_check, run_database_check


def database_validation():
    run_server_check()
    run_database_check()


def smtp_validation():
    # try:
    #     send_mail("[Database Backup] 확인 메일입니다.", f"{datetime.now()} 에 해당 계정으로 메일을 받도록 설정되었습니다. 백업 실패 및 백업 성공 메일을 해당 메일로 보내드립니다.")
    # except smtplib.SMTPException as e:
    #     logging.error("SMTP Validation Error: " + str(e))
    #     exit(0)
    # except Exception as e:
    #     logging.error("SMTP Validation Error: " + str(e))
    #     exit(0)
    pass

