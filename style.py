#!/usr/bin/python3
# style.py


PADDING = 10

RED = "\033[1;31m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36;1m"
GREEN = "\033[0;32;1m"
YELLOW = "\033[33;1m"
PURPLE = "\033[35m"
LIME = "\033[38;2;0;255;0m"

REVERSE = "\033[;7m"
RESET = "\033[0m"


def change_color(color):
    """"weather cli styling"""
    print (color, end="")