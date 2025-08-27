"""
Cropper module handles image cropping for the three screen positions
"""

from PIL import Image
from config import crop_params

def first_crop(image):
    """Apply first crop - 16% width × 22% height from left bottom"""
    width, height = image.size
    crop_width = int(width * 0.16)
    crop_height = int(height * 0.22)
    left = 0
    top = height - crop_height
    right = crop_width
    bottom = height
    return image.crop((left, top, right, bottom))

def shave_crop(image, position):
    """Apply position-specific shave crop"""
    params = crop_params[position]
    width, height = image.size
    left = int(width * params['shave_left'])
    top = int(height * params['shave_top'])
    right = width - int(width * params['shave_right'])
    bottom = height - int(height * params['shave_bottom'])
    return image.crop((left, top, right, bottom))

def crop_for_position(image, position):
    """Complete crop workflow for a position"""
    crop1 = first_crop(image)
    crop2 = shave_crop(crop1, position)
    return crop2

if __name__ == "__main__":
    # Test cropping with sample images
    import os
    os.makedirs("scr/test_results", exist_ok=True)
    for i in [1, 2, 3]:
        if os.path.exists(f"scr/{i}.png"):
            img = Image.open(f"scr/{i}.png")
            crop = crop_for_position(img, i)
            crop.save(f"scr/test_results/position_{i}_crop.png")
    print("Test crops saved in scr/test_results/")
