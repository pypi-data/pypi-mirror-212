"""Demo some functionalities of the board"""

from neopolitan.log import init_logger
from neopolitan.naples import Neopolitan
from neopolitan.board_functions.board_data import default_board_data
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
from neopolitan.board_functions.colors import *
# pylint: disable=anomalous-backslash-in-string

LOWER = 'abcdefghijklmnopqrstuvwxyz'
UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
NUMBERS = '0123456789'
SYMBOLS = '$ % ↑ ↓ ( ) - . , : = ~ ! @ & * ? < > ; | { } " \''

# todo: always passing events seems bad

def display(msg, events=None):
    """Display a message on the board"""

    init_logger()

    board_data = default_board_data.copy()
    board_data.message = msg

    # board_data.scroll_fast()

    neop = Neopolitan(board_data=board_data, events=events)
    neop.loop()
    del neop

def display_all(events=None):
    """Display all defined characters"""
    display(f'    {LOWER} {UPPER} {NUMBERS} {SYMBOLS}', events=events)

def display_all_lowercase_letters(events=None):
    """Display all lowercase letters"""
    display(LOWER, events=events)

def display_all_uppercase_letters(events=None):
    """Display all uppercase letters"""
    display(UPPER, events=events)

def display_all_numbers(events=None):
    """Display all numbers"""
    display(NUMBERS, events=events)

def display_all_symbols(events=None):
    """Display all symbols"""
    display(SYMBOLS, events=events)

def color_demo(events=None):
    """Displays a rainbow message"""
    msg = [
        ('-', WHITE),
        ('-', RED),
        ('-', ORANGE),
        ('-', YELLOW),
        ('-', GREEN),
        ('-', BLUE),
        ('-', PURPLE),
    ]
    display(msg, events=events)
