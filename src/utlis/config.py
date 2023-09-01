import os

import yaml
from dotenv import load_dotenv
from src.utlis.path import get_absolute_path

load_dotenv(get_absolute_path([".env"]))


class Config:
    def __init__(self):
        self.db_host = os.getenv("DB_HOST")
        self.db_port = os.getenv("DB_PORT")
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_name = os.getenv("DB_NAME")
        self.mailstorm_server = os.getenv("MAILSTORM_SERVER")
        self.mailstorm_port = int(os.getenv("MAILSTORM_PORT"))
        self.mailstorm_to = os.getenv("MAILSTORM_TO")
        self.data_expired_date = int(os.getenv("DATA_EXPIRED_DATE"))
        self.run_time = os.getenv("RUN_TIME")


configs = Config()


def load_config() -> Config:
    return configs
