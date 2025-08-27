"""
Screen capture module for MTA bot
Captures game window screenshots for cropping/OCR pipeline
"""

import mss
from PIL import Image
import pygetwindow as gw
import time
from config import WINDOW_TITLE

# Cache window info for performance
_cached_window_info = None

def get_cached_window_info():
    global _cached_window_info
    if _cached_window_info is None:
        windows = gw.getWindowsWithTitle(WINDOW_TITLE)
        if not windows:
            raise RuntimeError(f"Game window '{WINDOW_TITLE}' not found.")
        w = windows[0]
        border_left, border_top, border_right, border_bottom = 8, 31, 8, 8
        _cached_window_info = {
            'left': w.left + border_left,
            'top': w.top + border_top,
            'width': w.width - border_left - border_right,
            'height': w.height - border_top - border_bottom
        }
    return _cached_window_info

def capture_game_window():
    window_info = get_cached_window_info()
    with mss.mss() as sct:
        monitor = {
            'left': window_info['left'],
            'top': window_info['top'],
            'width': window_info['width'],
            'height': window_info['height']
        }
        screenshot = sct.grab(monitor)
        img = Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')
    return img

def reset_cache():
    global _cached_window_info
    _cached_window_info = None

if __name__ == "__main__":
    import os
    os.makedirs("scr", exist_ok=True)
    try:
        img = capture_game_window()
        img.save("scr/test_screenshot.png")
        print("✅ Screenshot saved: scr/test_screenshot.png")
    except Exception as e:
        print(f"❌ Screenshot failed: {e}")
