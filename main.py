"""
Main entry point for MTA Game Bot
"""

import sys
import os
from game_logic import GameBot

os.makedirs('scr', exist_ok=True)

def main():
    """Main function"""
    print("🎮 MTA Game Bot - ESP32 Edition")
    print("=" * 40)
    print("Bot workflow:")
    print("1. Press Left Alt")
    print("2. Process 3 positions: Left → Center → Right")
    print("3. For each position: Screenshot → Crop → OCR → Keypress")
    print("4. Take final screenshot")
    print("5. Wait and repeat")
    print("=" * 40)
    
    # Create debug directory
    os.makedirs("scr", exist_ok=True)
    
    # Get ESP32 COM port from command line if provided
    esp_port = sys.argv[1] if len(sys.argv) > 1 else None
    
    try:
        # Initialize bot
        bot = GameBot(esp_port=esp_port)
        
        if not bot.initialize():
            print("❌ Bot initialization failed")
            return
        
        # Test single cycle first
        print("\n🧪 Testing single cycle...")
        if bot.run_single_cycle():
            print("\n🎉 Single cycle test successful!")
            
            # Ask user for continuous mode
            response = input("\n🤔 Run continuous bot? (y/n): ").strip().lower()
            
            if response == 'y':
                bot.run_continuous()
            else:
                print("👋 Single test complete. Bot ready for use!")
        else:
            print("\n❌ Single cycle test failed")
            print("Check your setup:")
            print("1. ESP32-S3 connected and programmed")
            print("2. Game window open and titled 'MTA'")
            print("3. Tesseract OCR installed")
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        
    finally:
        print("🔚 Bot session ended")

if __name__ == "__main__":
    main()
