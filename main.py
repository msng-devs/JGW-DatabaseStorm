import logging
import time

import schedule
import yaml

from src.model.model import init_db
from src.utlis.log import setup_logging
from src.utlis.mysql_client import run_mysqldump
from src.utlis.validation import smtp_validation, database_validation


def main():
    with open('info.yaml') as f:
        conf = yaml.safe_load(f)

    setup_logging()

    # Config에 입력된 내용 체크
    logging.info("Start Validation config.yaml.....")

    logging.info("Start Validation smtp.....")
    smtp_validation()
    logging.info("smtp ok")

    logging.info("Start Validation database.....")
    database_validation()
    logging.info("database ok")

    logging.info("Finish Validation config.yaml.....")

    # 내부 database 설정
    logging.info("Start setup system.....")

    logging.info("Initialize database.....")
    init_db()
    logging.info("Finish setup system.....")

    logging.info("All process is finish! Now Start backup schedule.")
    schedule.every().day.at(conf["RUN_TIME"]).do(run_mysqldump)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
