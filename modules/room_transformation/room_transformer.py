
import base64
from io import BytesIO

import requests
from PIL import Image


# =====================================================
# CONFIGURATION
# =====================================================

DEFAULT_MODEL = "@cf/black-forest-labs/flux-1-schnell"

CLOUDFLARE_API_URL = (
    "https://api.cloudflare.com/client/v4/accounts/"
    "{account_id}/ai/run/{model}"
)


# =====================================================
# BUILD BEDROOM GENERATION PROMPT
# =====================================================

def build_room_prompt(
    room_type,
    interior_style,
    color_theme,
    custom_instructions=""
):
    """
    Build a detailed prompt for generating a new room.
    """

    prompt = f"""
Create a completely new, photorealistic {room_type} interior.

Interior design style: {interior_style}.
Preferred color palette: {color_theme}.

Design requirements:
- Beautiful and professionally designed interior.
- Realistic and elegant furniture.
- Comfortable and functional layout.
- Coordinated wall colors and decorative elements.
- Premium-looking materials and finishes.
- Beautiful ceiling and ambient lighting.
- Realistic shadows and natural lighting.
- Balanced furniture arrangement.
- High-quality interior photography.
- Wide-angle interior photography composition.

Additional requirements:
{custom_instructions}

The result must look like a real professionally designed
interior, not a drawing or illustration.
"""

    return prompt.strip()


# =====================================================
# GENERATE NEW ROOM USING CLOUDFLARE AI
# =====================================================

def transform_room(
    room_type,
    interior_style,
    color_theme,
    account_id,
    api_token,
    custom_instructions="",
    model=DEFAULT_MODEL
):
    """
    Generate a completely new room using
    Cloudflare Workers AI text-to-image.
    """

    if not account_id:
        raise ValueError("Cloudflare Account ID is missing.")

    if not api_token:
        raise ValueError("Cloudflare API token is missing.")

    prompt = build_room_prompt(
        room_type=room_type,
        interior_style=interior_style,
        color_theme=color_theme,
        custom_instructions=custom_instructions
    )

    url = CLOUDFLARE_API_URL.format(
        account_id=account_id,
        model=model
    )

    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": prompt,
        "steps": 4
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=180
        )

        if not response.ok:
            try:
                error_data = response.json()
            except ValueError:
                error_data = response.text

            raise RuntimeError(
                f"Cloudflare API error ({response.status_code}): "
                f"{error_data}"
            )

        result = response.json()

        image_data = result.get("result", {}).get("image")

        if not image_data:
            raise RuntimeError(
                "Cloudflare did not return an image. "
                f"Response: {result}"
            )

        image_bytes = base64.b64decode(image_data)

        generated_image = Image.open(
            BytesIO(image_bytes)
        ).convert("RGB")

        return generated_image

    except requests.exceptions.Timeout:
        raise RuntimeError(
            "Image generation timed out. Please try again."
        )

    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Unable to connect to Cloudflare. "
            "Check your internet connection."
        )
