import os

import yaml

config_file_path = '/bin/config/config.yaml'

with open(config_file_path) as f:
    configs = yaml.safe_load(f)


def load_config():
    return configs
