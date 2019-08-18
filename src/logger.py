import inspect
from datetime import datetime

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


def _log_base(title, title_color, *args):
    print(HEADER + str(datetime.now()) + ENDC + '\t' + title_color + BOLD + UNDERLINE + title + ENDC + '\t|\t', *args,
          flush=True)


def log_log(*args):
    _log_base('LOG', WARNING, *args)


def log_warn(*args):
    _log_base('WARNING', WARNING, *args)


def log_error(*args):
    _log_base('ERROR', FAIL, *args)


def log_info(*args):
    _log_base('INFO', OKBLUE, *args)


def log_success(*args):
    _log_base('SUCCESS', OKGREEN, *args)
