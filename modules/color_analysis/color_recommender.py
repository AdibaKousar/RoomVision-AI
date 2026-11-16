
COLOR_THEMES = {
    "Warm": {
        "Wall": "#F2E2CE",
        "Furniture": "#8B5E3C",
        "Accent": "#C76D4B",
        "Secondary": "#D9B99B",
        "Highlight": "#FFF4E6"
    },
    "Cool": {
        "Wall": "#E5EEF2",
        "Furniture": "#526D82",
        "Accent": "#7C9EAA",
        "Secondary": "#A9C3CE",
        "Highlight": "#F5FAFC"
    },
    "Neutral": {
        "Wall": "#E8E4DC",
        "Furniture": "#77736B",
        "Accent": "#B7A99A",
        "Secondary": "#CFC7BB",
        "Highlight": "#FAF9F6"
    },
    "Earthy": {
        "Wall": "#E8DCC8",
        "Furniture": "#765341",
        "Accent": "#A65F46",
        "Secondary": "#A9A078",
        "Highlight": "#F7F0E5"
    },
    "Luxury": {
        "Wall": "#E8DFD0",
        "Furniture": "#3D3538",
        "Accent": "#A88752",
        "Secondary": "#827078",
        "Highlight": "#F8F3E9"
    }
}


def recommend_color_theme(theme="Neutral"):
    """
    Return an interior color combination for a selected theme.
    """

    if theme not in COLOR_THEMES:
        raise ValueError(
            f"Unknown theme: {theme}. "
            f"Choose from {list(COLOR_THEMES.keys())}"
        )

    return {
        "theme": theme,
        "colors": COLOR_THEMES[theme]
    }


def get_available_themes():
    """Return all available color themes."""

    return list(COLOR_THEMES.keys())
