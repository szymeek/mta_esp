import pytesseract
from PIL import Image, ImageOps
import random
import cv2
import numpy as np

from config import OCR_WHITELIST, OCR_SCALE_FACTOR, TARGET_CHARACTERS, TESSERACT_PATH

# Configure Tesseract path
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def preprocess_for_ocr(pil_img):
    # Convert to grayscale
    gray = ImageOps.grayscale(pil_img)
    # Convert to OpenCV image
    open_cv = np.array(gray)
    # Adaptive thresholding for binarization
    thresh = cv2.adaptiveThreshold(
        open_cv, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 11, 2
    )
    # Convert back to PIL
    pil_thresh = Image.fromarray(thresh)
    # Scale up
    width, height = pil_thresh.size
    scaled = pil_thresh.resize(
        (width * OCR_SCALE_FACTOR, height * OCR_SCALE_FACTOR), 
        Image.LANCZOS
    )
    return scaled

def detect_character_fast(image):
    try:
        processed = preprocess_for_ocr(image)
        config = (
            f'-c tessedit_char_whitelist={OCR_WHITELIST} --psm 10 --dpi 300'
        )
        text = pytesseract.image_to_string(processed, config=config).strip()
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
    if len(sys.argv) > 1:
        img = Image.open(sys.argv[1])
        result = detect_character_fast(img)
        print(f"Detected character: {result['character']} (Confidence: {result['confidence']})")
    else:
        print("Usage: python ocr_module.py <imagefile>")
