"""
High-Level Keyboard Interface
Provides simple functions to press Alt, E, Q keys via ESP32
"""

from esp_serial import ESP32Serial

class KeyboardInterface:
    def __init__(self, esp_port: str = None):
        self.esp32 = ESP32Serial(port=esp_port)
        self.connected = False
    
    def initialize(self) -> bool:
        """Initialize ESP32 connection"""
        if self.esp32.auto_connect():
            self.connected = True
            print("🎮 Keyboard interface ready")
            return True
        else:
            print("❌ Failed to initialize keyboard interface")
            return False
    
    def press_alt(self) -> bool:
        """Press Left Alt key"""
        if not self.connected:
            print("❌ Keyboard not connected")
            return False
        
        print("⌨️  Pressing Alt key...")
        return self.esp32.send_command("ALT")
    
    def press_e(self) -> bool:
        """Press E key"""
        if not self.connected:
            print("❌ Keyboard not connected") 
            return False
        
        print("⌨️  Pressing E key...")
        return self.esp32.send_command("E")
    
    def press_q(self) -> bool:
        """Press Q key"""
        if not self.connected:
            print("❌ Keyboard not connected")
            return False
        
        print("⌨️  Pressing Q key...")
        return self.esp32.send_command("Q")
    
    def press_character_key(self, character: str) -> bool:
        """Press E or Q key based on detected character"""
        if character == 'E':
            return self.press_e()
        elif character == 'Q':
            return self.press_q()
        else:
            print(f"❌ Invalid character: {character}")
            return False
    
    def cleanup(self):
        """Clean up resources"""
        if self.esp32:
            self.esp32.disconnect()
            self.connected = False
