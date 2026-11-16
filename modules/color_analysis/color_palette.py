
from PIL import Image
import numpy as np
from collections import Counter


def extract_color_palette(image, num_colors=6):
    """
    Extract the most common colors from a room image.
    Returns HEX codes, RGB values and color proportions.
    """

    if not isinstance(image, Image.Image):
        image = Image.open(image)

    image = image.convert("RGB")
    image.thumbnail((300, 300))

    # Reduce colors for faster processing
    quantized = image.quantize(
        colors=num_colors,
        method=Image.Quantize.MEDIANCUT
    )

    palette = quantized.getpalette()
    color_counts = Counter(quantized.getdata())

    total_pixels = sum(color_counts.values())
    results = []

    for color_index, count in color_counts.most_common(num_colors):

        start = color_index * 3

        rgb = tuple(palette[start:start + 3])

        hex_color = "#{:02X}{:02X}{:02X}".format(*rgb)

        percentage = round(
            (count / total_pixels) * 100, 2
        )

        results.append({
            "hex": hex_color,
            "rgb": rgb,
            "percentage": percentage
        })

    return results
