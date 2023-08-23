import logging
import os
import sqlite3
from datetime import datetime, timedelta
import shutil
import yaml

from src.utlis.config import load_config
from src.utlis.path import get_absolute_path

conf = load_config()

db_file_path = get_absolute_path("/data/history.db")


def init_db():
    con = sqlite3.connect(db_file_path)
    cursor = con.cursor()
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='history'")
        table_exists = cursor.fetchone()

        if not table_exists:
            logging.info("Table is not Found. Init history table")
            cursor.execute('''CREATE TABLE history (
                                id INTEGER PRIMARY KEY,
                                run_date TEXT,
                                file TEXT,
                            )''')
            con.commit()
    except Exception as e:
        logging.error("Failed init DB. please check your './data' directory")

    finally:
        con.close()


def create_history(path: str) -> bool:
    con = sqlite3.connect(db_file_path)
    cursor = con.cursor()
    status = True
    try:
        run_date = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO history (run_date, file) VALUES (?, ?)", (run_date, path))
        con.commit()
    except Exception as e:
        logging.error("Failed create history")
        status = False
    finally:
        con.close()

    return status


def find_old_history():
    con = sqlite3.connect(db_file_path)
    cursor = con.cursor()
    try:
        current_time = datetime.now()
        target_time = current_time - timedelta(days=conf['DATA_EXPIRED_DATE'])

        cursor.execute("SELECT file FROM history WHERE run_date > ?",
                       (target_time.strftime("%Y-%m-%d")))
        con.commit()

        data = cursor.fetchall()

        for file_path in data:
            if os.path.exists(file_path):
                print(f"Remove Old Data: {file_path}")
                shutil.rmtree(file_path)
            else:
                print(f"File not found: {file_path}")

        cursor.execute("DELETE FROM history WHERE run_date > ?",
                       (target_time.strftime("%Y-%m-%d")))
        con.commit()
    except Exception as e:
        print(e)
        print("Failed find history")
    finally:
        con.close()
