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

# Delay between positions (seconds) - OPTIMIZED
POSITION_DELAY = 0.05  # Reduced from 0.3 to 0.05 seconds

# OCR configuration - OPTIMIZED
OCR_WHITELIST = "EQ"
OCR_SCALE_FACTOR = 4  # Reduced from 8 to 4 for faster processing
TARGET_CHARACTERS = ['E', 'Q']

# ESP32 Serial configuration
ESP32_BAUDRATE = 115200
ESP32_TIMEOUT = 2

# Tesseract OCR path (update if needed)
TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
