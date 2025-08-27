"""
Optimized main game logic with debug image saving for OCR diagnosis
"""

import time
import os
from screen_capture import capture_game_window
from cropper import crop_for_position
from ocr_module import detect_character_with_fallback
from keyboard_interface import KeyboardInterface
from config import CYCLE_DELAY, POSITION_DELAY

class GameBot:
    def __init__(self, esp_port=None):
        self.keyboard = KeyboardInterface(esp_port)
        self.cycle_count = 0
        self.running = False
        
        # Ensure debug folder exists
        os.makedirs("scr", exist_ok=True)
    
    def initialize(self) -> bool:
        """Initialize the bot"""
        if not self.keyboard.initialize():
            print("❌ Failed to initialize keyboard interface")
            return False
        
        print("🎮 MTA Game Bot initialized successfully (with debug saving)")
        return True
    
    def run_single_cycle(self) -> bool:
        """Run a single bot cycle with debug image saving"""
        self.cycle_count += 1
        print(f"\n🔄 Cycle #{self.cycle_count}")
        print("-" * 40)
        
        try:
            # Step 1: Press Left Alt
            print("Step 1: Pressing Left Alt...")
            if not self.keyboard.press_alt():
                return False
            
            time.sleep(POSITION_DELAY)
            
            # Steps 2-7: Process all three positions with debug save
            for position in [1, 2, 3]:
                print(f"\nStep {position + 1}: Processing position {position}")
                
                screenshot = capture_game_window()
                cropped_image = crop_for_position(screenshot, position)
                
                # Debug: Save cropped image being fed to OCR
                debug_filename = f"scr/debug_position_{position}.png"
                cropped_image.save(debug_filename)
                print(f"Saved debug crop: {debug_filename}")
                
                ocr_result = detect_character_with_fallback(cropped_image, debug=True)
                detected_char = ocr_result['character']
                confidence = ocr_result['confidence']
                
                print(f"   Detected: '{detected_char}' (confidence: {confidence})")
                
                if not self.keyboard.press_character_key(detected_char):
                    print(f"   ❌ Failed to send '{detected_char}' key")
                    return False
                
                print(f"   ✅ Sent '{detected_char}' key successfully")
                
                if position < 3:
                    time.sleep(POSITION_DELAY)
            
            # Step 8: Final screenshot (for future logic)
            print("\nStep 8: Taking final screenshot...")
            final_screenshot = capture_game_window()
            final_screenshot.save("scr/debug_final_screenshot.png")
            print("Saved final full screenshot for analysis")
            
            print(f"✅ Cycle #{self.cycle_count} completed successfully")
            return True
            
        except Exception as e:
            print(f"❌ Cycle #{self.cycle_count} failed: {e}")
            return False
    
    def run_continuous(self):
        """Run the bot continuously with debug saving"""
        print(f"🚀 Starting continuous bot mode (with debug saving)")
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
        """Clean up resources"""
        if self.keyboard:
            self.keyboard.cleanup()
        print("👋 Bot cleanup complete")

if __name__ == "__main__":
    bot = GameBot()
    if bot.initialize():
        bot.run_continuous()
