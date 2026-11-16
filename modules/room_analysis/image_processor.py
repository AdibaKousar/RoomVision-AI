
from PIL import Image
import numpy as np


def process_image(image_file, max_size=(1024, 1024)):
    """
    Prepare an uploaded room image for AI processing.
    """

    # Open uploaded image
    image = Image.open(image_file)

    # Store original information
    original_width, original_height = image.size
    original_format = image.format

    # Convert image to RGB
    processed_image = image.convert("RGB")

    # Resize while preserving aspect ratio
    processed_image.thumbnail(max_size)

    # Convert image into NumPy array
    image_array = np.array(processed_image)

    return {
        "image": processed_image,
        "image_array": image_array,
        "original_width": original_width,
        "original_height": original_height,
        "processed_width": processed_image.width,
        "processed_height": processed_image.height,
        "format": original_format
    }
