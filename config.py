"""
Configuration constants for MTA Bot
"""

# Crop parameters (final values)
crop_params = {
    1: {'shave_left': 0.17, 'shave_top': 0.16, 'shave_right': 0.70, 'shave_bottom': 0.63},
    2: {'shave_left': 0.16, 'shave_top': 0.16, 'shave_right': 0.71, 'shave_bottom': 0.63},
    3: {'shave_left': 0.45, 'shave_top': 0.16, 'shave_right': 0.42, 'shave_bottom': 0.63},
}

# Game window title
WINDOW_TITLE = "MTA"

# Delay between full cycles (seconds)
CYCLE_DELAY = 2.0

# Delay between positions (seconds)
POSITION_DELAY = 0.3

# OCR configuration
OCR_WHITELIST = "EQ"
OCR_SCALE_FACTOR = 8
TARGET_CHARACTERS = ['E', 'Q']

# ESP32 Serial configuration
ESP32_BAUDRATE = 115200
ESP32_TIMEOUT = 2

# Tesseract OCR path (update if needed)
TESSERACT_PATH = 'tesseract'

# Window borders for screenshot capture
WINDOW_BORDERS = {
    'left': 8,
    'top': 31,
    'right': 8,
    'bottom': 8
}

FIRST_CROP = {
    'width_percent': 16,
    'height_percent': 22,
    'position': 'left_bottom'
}

SECOND_CROP_SHAVING = {
    'left': 0.17,
    'top': 0.16,
    'right': 0.70,
    'bottom': 0.63
}
