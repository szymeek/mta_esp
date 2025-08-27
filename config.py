"""
Configuration constants with fixed float delays
"""

crop_params = {
    1: {'shave_left': 0.17, 'shave_top': 0.16, 'shave_right': 0.70, 'shave_bottom': 0.63},
    2: {'shave_left': 0.45, 'shave_top': 0.16, 'shave_right': 0.42, 'shave_bottom': 0.63},
    3: {'shave_left': 0.72, 'shave_top': 0.16, 'shave_right': 0.15, 'shave_bottom': 0.63},
}

WINDOW_TITLE = "MTA"

POSITION_DELAY = 0.3  # seconds between positions (fixed float)
CYCLE_DELAY = 3.0     # seconds between cycles (fixed float)

OCR_WHITELIST = "EQ"
OCR_SCALE_FACTOR = 8
TARGET_CHARACTERS = ['E', 'Q']

ESP32_BAUDRATE = 115200
ESP32_TIMEOUT = 2

TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
