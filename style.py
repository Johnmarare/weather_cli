#!/usr/bin/python3
# style.py


PADDING = 20

RED = "\033[1;31m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
YELLOW = "\033[33m"
PURPLE = "\033[35m"

REVERSE = "\033[;7m"
RESET = "\033[0m"


def change_color(color):
    """"weather cli styling"""
    print (color, end="")