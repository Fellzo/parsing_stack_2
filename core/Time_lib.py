import datetime
import time


def now():
    return time.time()


def date():
    return datetime.datetime.now()


def time_from_start():
    return "%.4f" % (now() - START_TIME)

START_TIME = now()
