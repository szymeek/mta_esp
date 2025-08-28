"""
Main game logic with OCR result CSV logging and detailed timing CSV logging
"""

import time
import os
from screen_capture import capture_game_window
from cropper import crop_for_position
from ocr_module import detect_character_fast as detect_character
from keyboard_interface import KeyboardInterface
from config import POSITION_DELAY, CYCLE_DELAY
from ocr_csv import append_ocr_result_to_csv
from timing_csv import append_timing_to_csv

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
        cycle_start = time.perf_counter()

        try:
            print("Step 1: Pressing Left Alt...")
            keypress_start = time.perf_counter()
            if not self.keyboard.press_alt():
                return False
            keypress_end = time.perf_counter()
            append_timing_to_csv("keypress_alt", self.cycle_count, None, keypress_end - keypress_start)

            position_delay_time = POSITION_DELAY()
            time.sleep(position_delay_time)
            append_timing_to_csv("position_delay", self.cycle_count, None, position_delay_time)

            for position in [1, 2, 3]:
                position_start = time.perf_counter()
                print(f"\nStep {position + 1}: Processing position {position}")

                screenshot_start = time.perf_counter()
                screenshot = capture_game_window()
                screenshot_end = time.perf_counter()
                append_timing_to_csv("screenshot", self.cycle_count, position, screenshot_end - screenshot_start)

                cropped_image_start = time.perf_counter()
                cropped_image = crop_for_position(screenshot, position)
                cropped_image_end = time.perf_counter()
                append_timing_to_csv("crop", self.cycle_count, position, cropped_image_end - cropped_image_start)

                debug_filename = f"scr/debug_position_{position}.png"
                cropped_image.save(debug_filename)
                print(f"Saved debug crop: {debug_filename}")

                ocr_start = time.perf_counter()
                ocr_result = detect_character(cropped_image)
                ocr_end = time.perf_counter()
                append_timing_to_csv("ocr", self.cycle_count, position, ocr_end - ocr_start)
                print(f"OCR full result: {ocr_result}")
                detected_char = ocr_result.get('character', None)
                if detected_char is None:
                    print("❌ OCR did not return 'character' key")
                    return False

                confidence = ocr_result.get('confidence', 'unknown')
                print(f"   Detected: '{detected_char}' (confidence: {confidence})")

                append_ocr_result_to_csv(self.cycle_count, position, detected_char, confidence)

                keypress_start = time.perf_counter()
                if not self.keyboard.press_character_key(detected_char):
                    print(f"   ❌ Failed to send '{detected_char}' key")
                    return False
                keypress_end = time.perf_counter()
                append_timing_to_csv("keypress", self.cycle_count, position, keypress_end - keypress_start)

                print(f"   ✅ Sent '{detected_char}' key successfully")

                if position < 3:
                    position_delay_time = POSITION_DELAY()
                    delay_start = time.perf_counter()
                    time.sleep(position_delay_time)
                    delay_end = time.perf_counter()
                    append_timing_to_csv("position_delay", self.cycle_count, position, delay_end - delay_start)
            print("\nStep 8: Taking final screenshot...")
            final_screen_start = time.perf_counter()
            final_screenshot = capture_game_window()
            final_screen_end = time.perf_counter()
            final_debug_filename = f"scr/debug_final_screenshot_{self.cycle_count}.png"
            final_screenshot.save(final_debug_filename)
            print(f"Saved final screenshot for cycle {self.cycle_count}")

            append_timing_to_csv("final_screenshot", self.cycle_count, None, final_screen_end - final_screen_start)

            cycle_end = time.perf_counter()
            append_timing_to_csv("cycle", self.cycle_count, None, cycle_end - cycle_start)

            print(f"✅ Cycle #{self.cycle_count} completed successfully")
            return True

        except Exception as e:
            print(f"❌ Cycle #{self.cycle_count} failed: {e}")
            return False

    def run_continuous(self):
        print(f"🚀 Starting continuous bot mode with timing logging")
        print(f"⏱️  Position delay: random {POSITION_DELAY()} seconds")
        print(f"⏱️  Cycle delay: random {CYCLE_DELAY()} seconds")
        print("🛑 Press Ctrl+C to stop")
        print("=" * 50)

        self.running = True

        try:
            while self.running:
                success = self.run_single_cycle()

                if not success:
                    print("❌ Cycle failed, stopping bot")
                    break

                cycle_delay = CYCLE_DELAY()
                delay_start = time.perf_counter()
                print(f"⏳ Waiting {cycle_delay:.2f} seconds before next cycle...")
                time.sleep(cycle_delay)
                delay_end = time.perf_counter()
                append_timing_to_csv("cycle_delay", self.cycle_count, None, delay_end - delay_start)

        except KeyboardInterrupt:
            print(f"\n🛑 Bot stopped by user after {self.cycle_count} cycles")
            self.running = False

        self.cleanup()

    def cleanup(self):
        if self.keyboard:
            self.keyboard.cleanup()
        print("👋 Bot cleanup complete")
