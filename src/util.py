# util.py

import os
import sys
import time

def get_console_dimen():
    rows, columns = os.popen("stty size", "r").read().split()
    return int(rows), int(columns)

def restart_line():
    _, cols = get_console_dimen()

    # Return to start
    sys.stdout.write("\r")
    sys.stdout.flush()

    # Clear line
    sys.stdout.write(" " * cols)
    sys.stdout.flush()

    # Return to start again
    sys.stdout.write("\r")
    sys.stdout.flush()
