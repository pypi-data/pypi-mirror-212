"""Handles LED board initialization and cleanup"""
# pylint: disable=import-error
# todo: handle tests in repo
import board as pinout # todo: make sure no import errors
import neopixel
# pylint: disable=no-name-in-module
# todo: why^?
from neopolitan.display.abstract_display import Display
from neopolitan.display.hardware_board_display import HardwareBoardDisplay
from neopolitan.board_functions.board import Board
from neopolitan.log import get_logger

class HardwareDisplay(Display):
    """Handles LED board initialization and cleanup"""

    def __init__(self, size):

        super().__init__()

        self.size = size

        # Initialize pixels
        get_logger().info('Initializing pixels')
        self.pixels = neopixel.NeoPixel(pinout.D10, self.size, brightness=0.01, auto_write=False)
        # Initialize board
        self.board_display = HardwareBoardDisplay(Board(size), self.pixels, size)

    def __del__(self):
        """Clean up neopixel"""
        get_logger().info('Deinitializing pixels')
        self.pixels.deinit()

    def draw(self):
        """Turn on/off all pixels"""
        self.board_display.draw_board()
        # tell the board to update itself
        self.pixels.show()

    def loop(self):
        """Drawing loop"""
        # todo: handle events

        self.draw()

        # todo: this is never true
        return self.should_exit
