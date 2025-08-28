#include <Arduino.h>
#include "USB.h"
#include "USBHIDKeyboard.h"

USBHIDKeyboard Keyboard;

void setup() {
  // Start USB as composite device (CDC + HID)
  USB.begin();
  Keyboard.begin();

  // Open CDC serial for commands from PC
  Serial.begin(115200);
  
  Serial.println("ESP32-S3 HID Keyboard Ready");
  Serial.println("Commands: ALT, Q, E");
}

void pressLeftAlt() {
  Keyboard.press(KEY_LEFT_ALT);
  delay(50);
  Keyboard.release(KEY_LEFT_ALT);
  Serial.println("Pressed Left Alt");
}

void pressQ() {
  Keyboard.press('q');
  delay(50);
  Keyboard.release('q');
  Serial.println("Pressed Q");
}

void pressE() {
  Keyboard.press('e');
  delay(50);
  Keyboard.release('e');
  Serial.println("Pressed E");
}

void loop() {
  // Check for commands on CDC
  static String buf;
  while (Serial.available()) {
    char c = (char)Serial.read();
    if (c == '\n' || c == '\r') {
      if (buf.length()) {
        String cmd = buf;
        buf = "";
        cmd.trim();
        cmd.toUpperCase();
        
        if (cmd == "ALT") {
          pressLeftAlt();
        } else if (cmd == "Q") {
          pressQ();
        } else if (cmd == "E") {
          pressE();
        } else {
          Serial.print("Unknown command: ");
          Serial.println(cmd);
          Serial.println("Valid commands: ALT, Q, E");
        }
      }
    } else {
      buf += c;
      // Avoid runaway memory on long noise
      if (buf.length() > 128) buf = "";
    }
  }

  delay(5);
}
