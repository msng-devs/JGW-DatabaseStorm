import os

current_working_directory = os.getcwd()

def get_absolute_path(path: str) -> str:
    return os.path.join(current_working_directory, path)