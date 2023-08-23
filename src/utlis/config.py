import os

import yaml

from src.utlis.path import get_absolute_path

config_file_path = get_absolute_path("/config/config.yaml")

with open(config_file_path) as f:
    configs = yaml.safe_load(f)


def load_config():
    return configs
