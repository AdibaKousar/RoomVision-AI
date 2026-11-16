
FURNITURE_DIMENSIONS = {
    "Bed": {"width": 6.5, "depth": 6.5},
    "Wardrobe": {"width": 5, "depth": 2},
    "Sofa": {"width": 7, "depth": 3},
    "Coffee Table": {"width": 3, "depth": 2},
    "Study Desk": {"width": 4, "depth": 2},
    "Dining Table": {"width": 5, "depth": 3},
    "Bookshelf": {"width": 3, "depth": 1.2},
    "TV Unit": {"width": 5, "depth": 1.5},
    "Bedside Table": {"width": 2, "depth": 1.5}
}


def calculate_room_area(room_width, room_length):
    if room_width <= 0 or room_length <= 0:
        raise ValueError("Room dimensions must be greater than zero.")

    return round(room_width * room_length, 2)


def get_furniture_dimensions(furniture_name):
    if furniture_name not in FURNITURE_DIMENSIONS:
        raise ValueError(f"Unknown furniture item: {furniture_name}")

    return FURNITURE_DIMENSIONS[furniture_name]


def calculate_furniture_area(furniture_items):
    total_area = 0

    for item in furniture_items:
        dimensions = get_furniture_dimensions(item)

        total_area += (
            dimensions["width"] * dimensions["depth"]
        )

    return round(total_area, 2)


def analyze_room_space(room_width, room_length, furniture_items):
    room_area = calculate_room_area(room_width, room_length)
    occupied_area = calculate_furniture_area(furniture_items)

    if occupied_area > room_area:
        utilization = 100
        available_area = 0
        warning = "Furniture area exceeds the available room area."
    else:
        utilization = round((occupied_area / room_area) * 100, 2)
        available_area = round(room_area - occupied_area, 2)
        warning = None

    if utilization < 35:
        recommendation = "Plenty of open space. You can consider adding useful furniture."
    elif utilization < 55:
        recommendation = "Balanced space usage. Maintain clear walking paths."
    elif utilization < 70:
        recommendation = "Room is becoming crowded. Review furniture placement."
    else:
        recommendation = "High space usage. Consider reducing or rearranging furniture."

    return {
        "room_area": room_area,
        "occupied_area": occupied_area,
        "available_area": available_area,
        "utilization_percentage": utilization,
        "recommendation": recommendation,
        "warning": warning
    }

def generate_furniture_layout(room_width, room_length, furniture_items):
    """
    Generate a simple wall-based furniture layout.
    Coordinates are measured in feet from the bottom-left corner.
    """

    if room_width <= 0 or room_length <= 0:
        raise ValueError("Room dimensions must be greater than zero.")

    placements = []
    occupied_rectangles = []

    margin = 0.5
    gap = 1.5

    current_x = margin
    current_y = margin
    row_depth = 0

    for item in sorted(
    furniture_items,
    key=lambda name: (
        get_furniture_dimensions(name)["width"]
        * get_furniture_dimensions(name)["depth"]
    ),
    reverse=True
):
        dimensions = get_furniture_dimensions(item)
        width = dimensions["width"]
        depth = dimensions["depth"]

        if width > room_width - 2 * margin:
            placements.append({
                "name": item,
                "status": "Does not fit",
                "x": None,
                "y": None,
                "width": width,
                "depth": depth
            })
            continue

        if current_x + width > room_width - margin:
            current_x = margin
            current_y += row_depth + gap
            row_depth = 0

        if current_y + depth > room_length - margin:
            placements.append({
                "name": item,
                "status": "No available placement",
                "x": None,
                "y": None,
                "width": width,
                "depth": depth
            })
            continue

        placement = {
            "name": item,
            "status": "Placed",
            "x": round(current_x, 2),
            "y": round(current_y, 2),
            "width": width,
            "depth": depth
        }

        placements.append(placement)
        occupied_rectangles.append(placement)

        current_x += width + gap
        row_depth = max(row_depth, depth)

    return placements

def create_floor_plan(room_width, room_length, placements):
    """
    Create a 2D floor plan using Plotly.
    Furniture positions are measured in feet.
    """
    import plotly.graph_objects as go

    fig = go.Figure()

    # Room boundary
    fig.add_shape(
        type="rect",
        x0=0,
        y0=0,
        x1=room_width,
        y1=room_length,
        line=dict(color="#49366F", width=4),
        fillcolor="#F7F4FC"
    )

    # Furniture rectangles
    for item in placements:
        if item["status"] != "Placed":
            continue

        x = item["x"]
        y = item["y"]
        width = item["width"]
        depth = item["depth"]

        fig.add_shape(
            type="rect",
            x0=x,
            y0=y,
            x1=x + width,
            y1=y + depth,
            line=dict(color="#49366F", width=2),
            fillcolor="#C9B7E8"
        )

        fig.add_annotation(
            x=x + width / 2,
            y=y + depth / 2,
            text=item["name"],
            showarrow=False,
            font=dict(size=11, color="#28243A")
        )

    fig.update_layout(
        title="AI-Assisted Room Furniture Layout",
        xaxis=dict(
            title="Room Width (feet)",
            range=[0, room_width],
            dtick=1,
            scaleanchor="y"
        ),
        yaxis=dict(
            title="Room Length (feet)",
            range=[0, room_length],
            dtick=1
        ),
        height=600,
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False
    )

    return fig
