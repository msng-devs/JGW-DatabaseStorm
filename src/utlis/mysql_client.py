import logging
import os
import subprocess
from datetime import datetime, time
import mysql.connector
import yaml

from src.model.model import create_history
from src.utlis.config import load_config
from src.utlis.mail import send_mail

conf = load_config()

root_directory = os.path.dirname(os.path.abspath(__file__))

mysql_host = conf['DB_HOST']
mysql_user = conf['DB_USER']
mysql_password = conf['DB_PASSWORD']
mysql_database = conf['DB_NAME']

mysql_connector_config = {
    'user': mysql_user,
    'password': mysql_password,
    'host': mysql_host,
    'database': mysql_database
}


# mysqldump를 수행하는 함수.
# 해당 스크립트가 동작할 컨테이너에는 mysqlclient가 설치되어있는데, 해당 클라이언트를 바탕으로 mysqldump를 수행한다.
def run_mysqldump():
    file_name = "/data/" + datetime.now().strftime("%Y-%m-%d") + "_bak"
    output_file = os.path.join(root_directory, file_name + "/backup.sql")
    os.makedirs(os.path.join(root_directory, file_name), exist_ok=True)

    #http://intomysql.blogspot.com/2010/12/mysqldump.html
    #참고
    mysqldump_cmd = [
        'mysqldump',
        'single-transaction',
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
        '--databases' + mysql_database
    ]

    try:
        with open(output_file, 'w') as f:
            subprocess.run(mysqldump_cmd, stdout=f, text=True, check=True)
        logging.info('Backup completed successfully.')
        history_result = create_history(output_file)

        if history_result:
            send_mail("[성공] Database Backup", f"{datetime.now()}에 실시한 성공적으로 백업을 완료하였습니다. 생성된 파일명 {output_file}")

        else:
            send_mail("[실패] Database Backup",
                      f"{datetime.now()}에 실시한 백업에서 파일은 성공적으로 저장했지만, 히스토리를 생성하는데 실패했습니다.")

    except subprocess.CalledProcessError as e:
        logging.info('Error occurred:', e)
        send_mail("[실패] Database Backup", f"{datetime.now()}에 실시한 백업을 실패했습니다. 에러 메시지: {str(e)}")


def run_server_check():
    try:
        connection = mysql.connector.connect(**mysql_connector_config)
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchall()

    except Exception as e:
        logging.error("Failed to connect to database")
        exit(0)


def run_database_check():
    try:
        connection = mysql.connector.connect(**mysql_connector_config)
        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES LIKE " + mysql_database)
        result = cursor.fetchall()
        result.index(mysql_database)

    except ValueError:
        logging.error("Database is not found")
        exit(0)

    except Exception as e:
        logging.error("Failed to connect to database")
        exit(0)
