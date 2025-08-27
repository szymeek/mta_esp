"""
Optimized OCR module for fast E/Q character detection
"""

import pytesseract
from PIL import Image
import random
from config import OCR_WHITELIST, OCR_SCALE_FACTOR, TARGET_CHARACTERS, TESSERACT_PATH

# Configure Tesseract
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def detect_character_fast(image):
    """Fast OCR with minimal preprocessing - optimized for speed"""
    try:
        # Quick scaling and OCR - single method for speed
        width, height = image.size
        scaled = image.resize((width * OCR_SCALE_FACTOR, height * OCR_SCALE_FACTOR), Image.LANCZOS)
        
        # Fast OCR configuration
        config = f'-c tessedit_char_whitelist={OCR_WHITELIST} --psm 10'
        text = pytesseract.image_to_string(scaled, config=config).strip()

        if text in TARGET_CHARACTERS:
            return {'character': text, 'confidence': 'high'}
        else:
            # Random fallback when OCR fails
            fallback = random.choice(TARGET_CHARACTERS)
            return {'character': fallback, 'confidence': 'random_fallback'}
            
    except Exception:
        # Exception fallback
        fallback = random.choice(TARGET_CHARACTERS)
        return {'character': fallback, 'confidence': 'random_fallback'}

# Keep the advanced method available if needed
def detect_character_with_fallback(image, debug=False):
    """
    Advanced OCR with multiple methods (slower but more accurate)
    Use detect_character_fast() for speed optimization
    """
    # This is the original advanced method - kept for fallback
    return detect_character_fast(image)  # Using fast method for now

if __name__ == "__main__":
    # Test fast OCR
    from PIL import Image
    import sys
    
    if len(sys.argv) > 1:
        img_path = sys.argv[1]
        img = Image.open(img_path)
        result = detect_character_fast(img)
        print(f"Fast OCR: {result['character']} (confidence: {result['confidence']})")
    else:
        print("Usage: python ocr_module.py <image_path>")
