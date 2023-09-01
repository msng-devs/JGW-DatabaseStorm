import subprocess
import sys
from prettytable import PrettyTable

from src.core.mysql_client import run_mysqldump
from src.utlis.log import setup_logging
from src.model.model import find_all, delete
from src.utlis.path import get_absolute_path

setup_logging()


def print_help():
    print("\nusage: [cmd] [args] \n")
    print("The following commands are available: \n")
    print("[fr] : run force backup. this is not include schedule")
    print("[history] [count] : show backup history")
    print("[rm] [id] : remove backup history and file")
    print("[ct] [time] : change schedule time")
    print("[help] or [?] : show this help message")
    print("[exit] : exit program")
    print("\n")


def update_env_file(file_path, key, value):
    updated = False
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            parts = line.strip().split('=')
            if len(parts) == 2 and parts[0] == key:
                lines[i] = f'{key}={value}\n'
                updated = True

        if not updated:
            lines.append(f'{key}={value}\n')

        with open(file_path, 'w') as f:
            f.writelines(lines)

        print(f'Updated .env file with {key}={value}')
    except Exception as e:
        print(f'Error: {e}')

    return updated


def stop_script():
    # main.py를 실행 중인 파이썬 프로세스를 찾아 종료합니다.
    subprocess.run(["pkill", "-f", "main.py"])
    print("Python script stopped.")


def start_script():
    # main.py를 다시 시작합니다.
    subprocess.run(["python3", "main.py"])
    print("Python script started.")


def run_cmd(cmd, args):
    if cmd == "help" or cmd == "?":
        print_help()


    elif cmd == "fr":
        try:
            run_mysqldump()
        except Exception as e:
            print(e)

    elif cmd == "history":
        cnt = args

        if cnt is None:
            cnt = 10

        result = find_all(cnt)

        if result is None or len(result) == 0:
            print("Not found mail history")
            return

        table = PrettyTable(["ID", "RUN DATE", "File Name"])

        for row in result:
            table.add_row([row[0], row[1], row[2]])

        print(table)

    elif cmd == "rm":
        status = delete(args)
        if status:
            print("Success remove history")
        else:
            print("Failed remove history")

    elif cmd == "ct":
        try:
            update_env_file(get_absolute_path(['.env']), 'RUN_TIME', args)
            print("Success change schedule time")
            stop_script()
            print("Kill System")
            start_script()
            print("Restart System")
            print("Success change schedule time")
        except Exception as e:
            print(e)

    elif cmd == "exit":
        print("Goodbye!")
        sys.exit(0)

    else:
        print("\nUnknown command: " + cmd)
        print_help()


def main():
    print("Welcome to databasestorm control system! Type 'help' or '?' to list commands. \n")
    while True:
        user_input = input("databasestorm> ")

        if user_input == "":
            continue

        split_input = user_input.split(" ")

        if len(split_input) == 1:
            run_cmd(split_input[0], None)
        else:
            run_cmd(split_input[0], split_input[1])


if __name__ == "__main__":
    main()
