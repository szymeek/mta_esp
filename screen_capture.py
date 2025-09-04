"""
Screenshot capture functionality using your provided code
"""

import mss
import pygetwindow as gw
from PIL import Image
import time

def find_and_activate_window(window_title):
    """Find and activate the game window"""
    windows = gw.getWindowsWithTitle(window_title)
    if not windows:
        raise Exception(f"No window found containing: '{window_title}'")
    
    w = windows[0]
    
    try:
        w.activate()
        w.restore()
        time.sleep(0.3)
    except Exception as e:
        print(f"Warning: Could not activate window: {e}")
    
    return w

def capture_game_window(window_title="MTA"):
    """
    Capture game window using your provided logic
    Returns: PIL Image of the full game content (borders removed)
    """
    # Find and activate window
    w = find_and_activate_window(window_title)
    
    # Calculate game area (remove window borders)
    WINDOW_BORDERS = {'left': 8, 'top': 31, 'right': 8, 'bottom': 8}
    game_left = w.left + WINDOW_BORDERS['left']
    game_top = w.top + WINDOW_BORDERS['top']
    game_width = w.width - WINDOW_BORDERS['left'] - WINDOW_BORDERS['right']
    game_height = w.height - WINDOW_BORDERS['top'] - WINDOW_BORDERS['bottom']
    
    # Take screenshot
    with mss.mss() as sct:
        monitor = {
            'left': game_left,
            'top': game_top,
            'width': game_width,
            'height': game_height
        }
        screenshot = sct.grab(monitor)
        full_image = Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')
    
    return full_image

if __name__ == "__main__":
    # Test screenshot capture
    import os
    os.makedirs("scr", exist_ok=True)
    wait_time = 3
    print(f"Taking screenshot in {wait_time} seconds... Switch to the game window!")
    time.sleep(wait_time)
    
    try:
        img = capture_game_window("MTA")
        img.save("scr/test_screenshot.png")
        print(f"✅ Screenshot saved: scr/test_screenshot.png ({img.size})")
    except Exception as e:
        print(f"❌ Screenshot failed: {e}")
