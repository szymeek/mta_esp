"""
Main game logic with OCR result CSV logging
"""

import time
import os
from screen_capture import capture_game_window
from cropper import crop_for_position
from ocr_module import detect_character_fast as detect_character
from keyboard_interface import KeyboardInterface
from config import POSITION_DELAY, CYCLE_DELAY
from ocr_csv import append_ocr_result_to_csv

class GameBot:
    def __init__(self, esp_port=None):
        self.keyboard = KeyboardInterface(esp_port)
        self.cycle_count = 0
        self.running = False

        os.makedirs("scr", exist_ok=True)

    def initialize(self) -> bool:
        if not self.keyboard.initialize():
            print("❌ Failed to initialize keyboard interface")
            return False
        print("🎮 MTA Game Bot initialized successfully")
        return True

    def run_single_cycle(self) -> bool:
        self.cycle_count += 1
        print(f"\n🔄 Cycle #{self.cycle_count}")
        print("-" * 40)

        try:
            print("Step 1: Pressing Left Alt...")
            if not self.keyboard.press_alt():
                return False

            time.sleep(POSITION_DELAY)

            for position in [1, 2, 3]:
                print(f"\nStep {position + 1}: Processing position {position}")
                screenshot = capture_game_window()
                cropped_image = crop_for_position(screenshot, position)

                debug_filename = f"scr/debug_position_{position}.png"
                cropped_image.save(debug_filename)
                print(f"Saved debug crop: {debug_filename}")

                ocr_result = detect_character(cropped_image)
                print(f"OCR full result: {ocr_result}")
                detected_char = ocr_result.get('character', None)
                if detected_char is None:
                    print("❌ OCR did not return 'character' key")
                    return False

                confidence = ocr_result.get('confidence', 'unknown')

                print(f"   Detected: '{detected_char}' (confidence: {confidence})")

                # Log OCR result to CSV
                append_ocr_result_to_csv(self.cycle_count, position, detected_char, confidence)

                if not self.keyboard.press_character_key(detected_char):
                    print(f"   ❌ Failed to send '{detected_char}' key")
                    return False

                print(f"   ✅ Sent '{detected_char}' key successfully")

                if position < 3:
                    time.sleep(POSITION_DELAY)

            print("\nStep 8: Taking final screenshot...")
            final_screenshot = capture_game_window()
            final_screenshot.save(f"scr/debug_final_screenshot_{self.cycle_count}.png")

            print(f"✅ Cycle #{self.cycle_count} completed successfully")
            return True

        except Exception as e:
            print(f"❌ Cycle #{self.cycle_count} failed: {e}")
            return False

    def run_continuous(self):
        print(f"🚀 Starting continuous bot mode")
        print(f"⏱️ Cycle delay: {CYCLE_DELAY} seconds")
        print(f"⚡ Position delay: {POSITION_DELAY} seconds")
        print("🛑 Press Ctrl+C to stop")
        print("=" * 50)

        self.running = True

        try:
            while self.running:
                success = self.run_single_cycle()

                if not success:
                    print("❌ Cycle failed, stopping bot")
                    break

                print(f"⏳ Waiting {CYCLE_DELAY} seconds before next cycle...")
                time.sleep(CYCLE_DELAY)

        except KeyboardInterrupt:
            print(f"\n🛑 Bot stopped by user after {self.cycle_count} cycles")
            self.running = False

        self.cleanup()

    def cleanup(self):
        if self.keyboard:
            self.keyboard.cleanup()
        print("👋 Bot cleanup complete")
