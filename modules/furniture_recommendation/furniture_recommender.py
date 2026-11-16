
FURNITURE_DATABASE = {
    "Bedroom": [
        {
            "name": "Platform Bed",
            "category": "Bed",
            "style": ["Modern", "Minimalist", "Scandinavian"],
            "price": 18000,
            "description": "A clean, low-profile bed for a contemporary bedroom."
        },
        {
            "name": "Wardrobe",
            "category": "Storage",
            "style": ["Modern", "Traditional", "Minimalist"],
            "price": 15000,
            "description": "Practical clothing storage with a simple finish."
        },
        {
            "name": "Bedside Table",
            "category": "Table",
            "style": ["Modern", "Scandinavian", "Traditional"],
            "price": 4500,
            "description": "A compact table for essentials beside the bed."
        },
        {
            "name": "Accent Chair",
            "category": "Seating",
            "style": ["Modern", "Bohemian", "Traditional"],
            "price": 7500,
            "description": "Additional seating for a bedroom corner."
        }
    ],

    "Living Room": [
        {
            "name": "Three-Seater Sofa",
            "category": "Seating",
            "style": ["Modern", "Traditional", "Scandinavian"],
            "price": 28000,
            "description": "Comfortable seating for family and guests."
        },
        {
            "name": "Coffee Table",
            "category": "Table",
            "style": ["Modern", "Minimalist", "Industrial"],
            "price": 6500,
            "description": "A central surface for a living room seating area."
        },
        {
            "name": "TV Unit",
            "category": "Storage",
            "style": ["Modern", "Minimalist", "Industrial"],
            "price": 12000,
            "description": "Organized storage and display for entertainment equipment."
        },
        {
            "name": "Bookshelf",
            "category": "Storage",
            "style": ["Scandinavian", "Traditional", "Industrial"],
            "price": 8500,
            "description": "Display books and decorative objects."
        }
    ],

    "Kitchen": [
        {
            "name": "Kitchen Storage Cabinet",
            "category": "Storage",
            "style": ["Modern", "Traditional", "Minimalist"],
            "price": 14000,
            "description": "Organized storage for kitchen essentials."
        },
        {
            "name": "Kitchen Island",
            "category": "Workspace",
            "style": ["Modern", "Industrial", "Scandinavian"],
            "price": 22000,
            "description": "Additional preparation and serving space."
        },
        {
            "name": "Dining Table",
            "category": "Table",
            "style": ["Modern", "Traditional", "Scandinavian"],
            "price": 16000,
            "description": "A dedicated dining surface for everyday meals."
        }
    ],

    "Study Room": [
        {
            "name": "Study Desk",
            "category": "Workspace",
            "style": ["Modern", "Minimalist", "Industrial"],
            "price": 8500,
            "description": "A functional surface for studying and working."
        },
        {
            "name": "Ergonomic Chair",
            "category": "Seating",
            "style": ["Modern", "Minimalist", "Industrial"],
            "price": 6500,
            "description": "An adjustable chair designed for desk work."
        },
        {
            "name": "Book Storage Unit",
            "category": "Storage",
            "style": ["Scandinavian", "Traditional", "Modern"],
            "price": 7000,
            "description": "Organized storage for books and stationery."
        }
    ]
}


def recommend_furniture(
    room_type,
    interior_style,
    budget=None,
    categories=None
):
    """
    Recommend furniture using room type, style and budget.

    Prices are illustrative estimates in INR, not live market quotes.
    """

    if room_type not in FURNITURE_DATABASE:
        raise ValueError(f"Unsupported room type: {room_type}")

    recommendations = []

    for item in FURNITURE_DATABASE[room_type]:

        style_match = interior_style in item["style"]

        category_match = (
            not categories or item["category"] in categories
        )

        budget_match = (
            budget is None or item["price"] <= budget
        )

        if style_match and category_match and budget_match:

            recommendations.append({
                **item,
                "style_match": True
            })

    return recommendations


def get_available_room_types():
    return list(FURNITURE_DATABASE.keys())


def get_available_styles():
    return [
        "Modern",
        "Minimalist",
        "Scandinavian",
        "Traditional",
        "Bohemian",
        "Industrial"
    ]
