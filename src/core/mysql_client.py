import logging
import os
import subprocess
from datetime import datetime, time
import mysql.connector
import yaml

from src.model.model import create_history
from src.utlis.config import load_config
from src.utlis.mail import send_mail
from src.utlis.path import get_absolute_path

confing = load_config()

root_directory = os.path.dirname(os.path.abspath(__file__))

mysql_host = confing.db_host
mysql_user = confing.db_user
mysql_password = confing.db_password
mysql_database = confing.db_name
mysql_port = confing.db_port


# mysqldump를 수행하는 함수.
# 해당 스크립트가 동작할 컨테이너에는 mysqlclient가 설치되어있는데, 해당 클라이언트를 바탕으로 mysqldump를 수행한다.
def run_mysqldump():
    output_directory = get_absolute_path(
        ['data', f'{mysql_database}_{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}_backup'])
    os.makedirs(output_directory, exist_ok=True)
    output_file_name = os.path.join(output_directory, "backup.sql")

    # 사용된 Flag들은 다음 링크를 참고 http://intomysql.blogspot.com/2010/12/mysqldump.html
    mysqldump_cmd = [
        'mysqldump',
        '--single-transaction',
        '--skip-opt',
        '--extended-insert',
        '--add-drop-database',
        '--add-drop-table',
        '--no-create-db',
        '--no-create-info',
        '--default-character-set=utf8',
        '--quick',
        '--host=' + mysql_host,
        '--user=' + mysql_user,
        '--password=' + mysql_password,
        '--port=' + str(mysql_port),
        mysql_database
    ]

    try:
        with open(output_file_name, 'w') as f:
            subprocess.run(mysqldump_cmd, stdout=f, text=True, check=True)
        logging.info('Backup completed successfully.')
        history_result = create_history(output_directory)

        if history_result:
            send_mail("[DatabaseStorm] Database Backup에 성공했습니다.", f"{datetime.now()}에 실시한 성공적으로 백업을 완료하였습니다. 생성된 파일명 {output_directory}")

        else:
            send_mail("[DatabaseStorm] Database Backup에 실패했습니다.",
                      f"{datetime.now()}에 실시한 백업에서 파일은 성공적으로 저장했지만, 히스토리를 생성하는데 실패했습니다.")

    except subprocess.CalledProcessError as e:
        logging.info('Error occurred:', e)
        send_mail("[DatabaseStorm] Database Backup에 실패했습니다.", f"{datetime.now()}에 실시한 백업을 실패했습니다. 에러 메시지: {str(e)}")


# 입력된 데이터베이스 서버 정보가 유효한지 검증하는 함수
def run_server_check():
    try:
        logging.info(f"Start Connect to database {mysql_host}")
        connection = mysql.connector.connect(host=mysql_host, user=mysql_user, password=mysql_password,
                                             port=int(mysql_port))
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchall()

    except Exception as e:
        logging.error("Failed to connect to database server > " + str(e))
        exit(0)


# 입력된 데이터베이스가 유효한지 검증하는 함수
def run_database_check():
    try:
        connection = mysql.connector.connect(host=mysql_host, user=mysql_user, password=mysql_password,
                                             port=int(mysql_port))
        cursor = connection.cursor()
        cursor.execute(f"SELECT 1 FROM Information_schema.tables WHERE table_schema = '{mysql_database}'")
        result = cursor.fetchall()
        assert len(result) > 0

    except AssertionError as e:
        logging.error("Database is not found")
        exit(0)

    except Exception as e:
        logging.error("Failed to connect to check database > " + str(e))
        exit(0)
