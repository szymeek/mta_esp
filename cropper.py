"""
Cropper module for image cropping per position
"""

from PIL import Image

# Your final crop parameters
crop_params = {
    1: {'shave_left': 0.17, 'shave_top': 0.16, 'shave_right': 0.70, 'shave_bottom': 0.63},
    2: {'shave_left': 0.45, 'shave_top': 0.16, 'shave_right': 0.42, 'shave_bottom': 0.63},
    3: {'shave_left': 0.72, 'shave_top': 0.16, 'shave_right': 0.15, 'shave_bottom': 0.63},
}

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
