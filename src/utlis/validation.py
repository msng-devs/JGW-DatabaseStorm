import logging
import smtplib
from datetime import datetime

from src.utlis.mail import send_mail
from src.utlis.mysql_client import run_server_check, run_database_check
from src.utlis.config import load_config


# DB_HOST:
# DB_PORT:
# DB_USER:
# DB_PASSWORD:
# DB_NAME:
# DATA_EXPIRED_DATE:
# RUN_TIME:
def config_file_validation():
    configs = load_config()

    if not configs:
        logging.error("config file is null")
        exit(0)

    if not configs["DB_HOST"]:
        logging.error("DB_HOST is null")
        exit(0)

    if not configs["DB_PORT"]:
        logging.error("DB_PORT is null")
        exit(0)

    if not configs["DB_USER"]:
        logging.error("DB_USER is null")
        exit(0)

    if not configs["DB_PASSWORD"]:
        logging.error("DB_PASSWORD is null")
        exit(0)

    if not configs["DB_NAME"]:
        logging.error("DB_NAME is null")
        exit(0)

    if not configs["DATA_EXPIRED_DATE"]:
        logging.error("DATA_EXPIRED_DATE is null")
        exit(0)

    if not configs["RUN_TIME"]:
        logging.error("RUN_TIME is null")
        exit(0)


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
