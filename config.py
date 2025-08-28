"""
Configuration constants with random delay ranges and delay functions
"""

import random

crop_params = {
    1: {'shave_left': 0.17, 'shave_top': 0.16, 'shave_right': 0.70, 'shave_bottom': 0.63},
    2: {'shave_left': 0.45, 'shave_top': 0.16, 'shave_right': 0.42, 'shave_bottom': 0.63},
    3: {'shave_left': 0.72, 'shave_top': 0.16, 'shave_right': 0.15, 'shave_bottom': 0.63},
}

WINDOW_TITLE = "MTA"

# Random Delay Ranges
POSITION_DELAY_MIN = 0.29
POSITION_DELAY_MAX = 0.31
CYCLE_DELAY_MIN = 2.8
CYCLE_DELAY_MAX = 3.1

# Delay functions that return random float values
POSITION_DELAY = lambda: random.uniform(POSITION_DELAY_MIN, POSITION_DELAY_MAX)
CYCLE_DELAY = lambda: random.uniform(CYCLE_DELAY_MIN, CYCLE_DELAY_MAX)

# OCR settings
OCR_WHITELIST = "EQ"
OCR_SCALE_FACTOR = 8
TARGET_CHARACTERS = ['E', 'Q']

ESP32_BAUDRATE = 115200
ESP32_TIMEOUT = 2

TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
