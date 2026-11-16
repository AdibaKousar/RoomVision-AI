
BUDGET_CATEGORIES = {
    "Furniture": {
        "Bed": 18000,
        "Sofa": 28000,
        "Wardrobe": 15000,
        "Dining Table": 16000,
        "Study Desk": 8500,
        "Coffee Table": 6500,
        "TV Unit": 12000
    },

    "Painting": {
        "Wall Painting": 25,
        "Texture Painting": 45,
        "Ceiling Painting": 20
    },

    "Flooring": {
        "Vitrified Tiles": 90,
        "Wooden Flooring": 150,
        "Marble Flooring": 250
    },

    "Lighting": {
        "LED Ceiling Light": 1200,
        "Pendant Light": 2500,
        "Wall Light": 1500,
        "Floor Lamp": 3000
    },

    "Decor": {
        "Curtains": 2500,
        "Wall Art": 2000,
        "Indoor Plant": 800,
        "Decorative Mirror": 3500,
        "Rug": 4000
    },

    "Labor": {
        "Painting Labor": 15,
        "Flooring Installation": 35,
        "Furniture Installation": 1500
    }
}


def calculate_budget(selected_items, room_area=100):
    """
    Calculate an estimated interior design budget.

    selected_items example:
    {
        "Furniture": {"Bed": 1, "Wardrobe": 1},
        "Painting": {"Wall Painting": 4}
    }

    Painting and flooring rates are per square foot.
    Labor rates are either per square foot or per installation.
    """

    if room_area <= 0:
        raise ValueError("Room area must be greater than zero.")

    breakdown = {}
    grand_total = 0

    for category, items in selected_items.items():

        if category not in BUDGET_CATEGORIES:
            raise ValueError(f"Unknown category: {category}")

        for item_name, quantity in items.items():

            if item_name not in BUDGET_CATEGORIES[category]:
                raise ValueError(f"Unknown item: {item_name}")

            if not isinstance(quantity, int) or isinstance(quantity, bool):
                raise ValueError("Quantity must be a whole number.")

            if quantity < 0:
                raise ValueError("Quantity cannot be negative.")

            rate = BUDGET_CATEGORIES[category][item_name]

            if category in ["Painting", "Flooring"]:
                amount = rate * room_area * quantity

            elif category == "Labor" and item_name in [
                "Painting Labor",
                "Flooring Installation"
            ]:
                amount = rate * room_area * quantity

            else:
                amount = rate * quantity

            breakdown[item_name] = {
                "category": category,
                "rate": rate,
                "quantity": quantity,
                "amount": amount
            }

            grand_total += amount

    return {
        "breakdown": breakdown,
        "grand_total": grand_total,
        "room_area": room_area
    }


def get_budget_categories():
    return BUDGET_CATEGORIES
