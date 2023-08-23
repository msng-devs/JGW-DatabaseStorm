import os

# current_working_directory = os.getcwd()


def get_absolute_path(path: str) -> str:
    return os.path.join('/app', path)
