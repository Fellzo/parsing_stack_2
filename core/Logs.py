"""
    Logs.py
    Запись логов в файл
"""
import core.Time_lib as Time_lib

LOGS_FILE_NAME = "logs.txt"
logs_file = open(LOGS_FILE_NAME, "a")


def add_log(log):
    logs_file.writelines(str(Time_lib.date()) + " " + log + "\n")

