"""
Optimized OCR module for E/Q character detection with full file content
"""

import pytesseract
from PIL import Image
import random
from config import OCR_WHITELIST, OCR_SCALE_FACTOR, TARGET_CHARACTERS, TESSERACT_PATH

# Configure Tesseract
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def detect_character_fast(image):
    """Fast OCR with minimal preprocessing"""
    try:
        width, height = image.size
        scaled = image.resize((width * OCR_SCALE_FACTOR, height * OCR_SCALE_FACTOR), Image.LANCZOS)
        config = f'-c tessedit_char_whitelist={OCR_WHITELIST} --psm 10'
        text = pytesseract.image_to_string(scaled, config=config).strip()

        if text in TARGET_CHARACTERS:
            return {'character': text, 'confidence': 'high'}
        else:
            fallback = random.choice(TARGET_CHARACTERS)
            return {'character': fallback, 'confidence': 'random_fallback'}
    except Exception:
        fallback = random.choice(TARGET_CHARACTERS)
        return {'character': fallback, 'confidence': 'random_fallback'}

if __name__ == "__main__":
    import sys
    from PIL import Image
    if len(sys.argv) > 1:
        img = Image.open(sys.argv[1])
        result = detect_character_fast(img)
        print(f"Detected character: {result['character']} (Confidence: {result['confidence']})")
    else:
        print("Usage: python ocr_module.py <image_path>")
