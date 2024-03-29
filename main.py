import logging
import time
from datetime import datetime

import schedule

from src.model.model import init_db
from src.utlis.config import load_config
from src.utlis.log import setup_logging
from src.core.mysql_client import run_mysqldump
from src.utlis.mailstorm import send_mail
from src.utlis.validation import database_validation


def main():
    # 로그 설정
    setup_logging()

    # /app/config/config.yaml 파일을 로드합니다.
    conf = load_config()

    logging.info("Start Validation mailstorm.....")
    send_mail("[DatabaseStorm] 확인 메일입니다.", f"{datetime.now()} 에 해당 계정으로 메일을 받도록 설정되었습니다. 백업 실패 및 백업 성공 메일을 해당 메일로 보내드립니다.")
    logging.info("mailstorm ok")

    # 입력된 백업 대상 데이터베이스의 정보를 검증합니다.
    logging.info("Start Validation database.....")
    database_validation()
    logging.info("database ok")

    logging.info("Finish Validation config.yaml.....")

    # 내부 database 설정, 백업 히스토리 및 파일 관리를 위해 sqlite3를 구성합니다.
    logging.info("Start setup system.....")

    logging.info("Initialize database.....")
    init_db()
    logging.info("Finish setup system.....")

    logging.info(f"All process is finish! Now Start backup schedule. > {conf.run_time}")
    schedule.every().day.at(str(conf.run_time)).do(run_mysqldump)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
