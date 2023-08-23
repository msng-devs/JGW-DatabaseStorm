import os

import yaml

root_directory = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(root_directory, '/config/config.yaml')

with open(config_file_path) as f:
    configs = yaml.safe_load(f)


def load_config():
    return configs
