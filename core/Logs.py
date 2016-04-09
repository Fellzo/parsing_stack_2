import core.Time_lib

LOGS_FILE_NAME = "logs.txt"
logs_file = open(LOGS_FILE_NAME, "a")


def add_log(log):
    logs_file.writelines(str(core.Time_lib.date()) + " " + log + "\n")

