
import numpy as np
from PIL import Image


def analyze_room_style(image):
    """
    Estimate interior design style using visual color features.
    This is an initial rule-based classifier, not a trained AI model.
    """

    if not isinstance(image, Image.Image):
        image = Image.open(image)

    image = image.convert("RGB")
    image.thumbnail((256, 256))

    pixels = np.asarray(image, dtype=np.float32) / 255.0
    pixels = pixels.reshape(-1, 3)

    # Calculate visual characteristics
    brightness = np.mean(pixels)
    saturation = np.mean(
        np.max(pixels, axis=1) - np.min(pixels, axis=1)
    )
    contrast = np.std(pixels)

    # Estimate neutral and warm color proportions
    max_channel = np.max(pixels, axis=1)
    min_channel = np.min(pixels, axis=1)
    neutral_ratio = np.mean((max_channel - min_channel) < 0.18)

    warm_ratio = np.mean(
        (pixels[:, 0] > pixels[:, 2] * 1.15)
        & (pixels[:, 0] > pixels[:, 1] * 0.85)
    )

    scores = {
        "Minimalist": 0,
        "Scandinavian": 0,
        "Modern": 0,
        "Traditional": 0,
        "Bohemian": 0,
        "Industrial": 0
    }

    # Initial rule-based scoring
    if neutral_ratio > 0.55:
        scores["Minimalist"] += 3
        scores["Scandinavian"] += 2
        scores["Modern"] += 2

    if brightness > 0.58:
        scores["Scandinavian"] += 3
        scores["Minimalist"] += 2

    if saturation < 0.25:
        scores["Minimalist"] += 2
        scores["Modern"] += 2
        scores["Industrial"] += 1

    if warm_ratio > 0.35:
        scores["Traditional"] += 2
        scores["Bohemian"] += 2
        scores["Scandinavian"] += 1

    if saturation > 0.38:
        scores["Bohemian"] += 3

    if contrast > 0.22:
        scores["Industrial"] += 2
        scores["Modern"] += 1

    ranked_styles = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    best_style = ranked_styles[0][0]
    total_score = sum(scores.values())

    confidence = (
        round((ranked_styles[0][1] / total_score) * 100, 2)
        if total_score > 0 else 0
    )

    return {
        "style": best_style,
        "confidence": confidence,
        "all_scores": dict(ranked_styles),
        "visual_features": {
            "brightness": round(float(brightness), 3),
            "saturation": round(float(saturation), 3),
            "contrast": round(float(contrast), 3),
            "neutral_color_ratio": round(float(neutral_ratio), 3),
            "warm_color_ratio": round(float(warm_ratio), 3)
        }
    }
