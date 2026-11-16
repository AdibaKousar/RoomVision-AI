
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


def generate_furniture_layout(
    room_width,
    room_length,
    furniture_items,
    clearance=1.5
):
    """
    Generate a furniture layout using candidate-position search.
    Coordinates are measured in feet from the bottom-left corner.
    """

    if room_width <= 0 or room_length <= 0:
        raise ValueError("Room dimensions must be greater than zero.")

    if clearance < 0:
        raise ValueError("Clearance cannot be negative.")

    margin = 0.5
    placements = []

    # Place larger furniture first
    sorted_items = sorted(
        furniture_items,
        key=lambda name: (
            get_furniture_dimensions(name)["width"]
            * get_furniture_dimensions(name)["depth"]
        ),
        reverse=True
    )

    def overlaps(x, y, width, depth, existing):
        for placed in existing:

            horizontal_gap = (
                x + width <= placed["x"] - clearance
                or x >= placed["x"] + placed["width"] + clearance
            )

            vertical_gap = (
                y + depth <= placed["y"] - clearance
                or y >= placed["y"] + placed["depth"] + clearance
            )

            if not (horizontal_gap or vertical_gap):
                return True

        return False

    for item in sorted_items:

        dimensions = get_furniture_dimensions(item)

        original_width = dimensions["width"]
        original_depth = dimensions["depth"]

        orientations = [
            (original_width, original_depth, 0),
            (original_depth, original_width, 90)
        ]

        best_position = None
        best_score = float("inf")

        for width, depth, rotation in orientations:

            if (
                width > room_width - 2 * margin
                or depth > room_length - 2 * margin
            ):
                continue

            # Search possible positions on a half-foot grid
            x = margin

            while x + width <= room_width - margin:

                y = margin

                while y + depth <= room_length - margin:

                    if not overlaps(
                        x, y, width, depth, placements
                    ):

                        # Prefer positions close to room walls
                        wall_distance = min(
                            x,
                            y,
                            room_width - (x + width),
                            room_length - (y + depth)
                        )

                        score = (
                            wall_distance * 10
                            + y * 0.1
                            + x * 0.01
                        )

                        if score < best_score:
                            best_score = score

                            best_position = {
                                "name": item,
                                "status": "Placed",
                                "x": round(x, 2),
                                "y": round(y, 2),
                                "width": width,
                                "depth": depth,
                                "rotation": rotation
                            }

                    y += 0.5

                x += 0.5

        if best_position:

            placements.append(best_position)

        else:

            placements.append({
                "name": item,
                "status": "No available placement",
                "x": None,
                "y": None,
                "width": original_width,
                "depth": original_depth,
                "rotation": 0
            })

    return placements



def create_floor_plan(room_width, room_length, placements, openings=None):
    """
    Create an interactive 2D furniture floor plan.
    Displays furniture dimensions, rotation and placement status.
    """
    if openings is None:
        openings = []

    import plotly.graph_objects as go

    fig = go.Figure()

    # ROOM BACKGROUND
    fig.add_shape(
        type="rect",
        x0=0,
        y0=0,
        x1=room_width,
        y1=room_length,
        line=dict(color="#49366F", width=4),
        fillcolor="#F7F4FC",
        layer="below"
    )

    # ROOM DIMENSIONS
    fig.add_annotation(
        x=room_width / 2,
        y=room_length + 0.35,
        text=f"Width: {room_width} ft",
        showarrow=False,
        font=dict(size=13, color="#49366F")
    )

    fig.add_annotation(
        x=room_width + 0.35,
        y=room_length / 2,
        text=f"Length: {room_length} ft",
        textangle=-90,
        showarrow=False,
        font=dict(size=13, color="#49366F")
    )

    # FURNITURE COLORS
    furniture_colors = {
        "Bed": "#B39DDB",
        "Wardrobe": "#90CAF9",
        "Sofa": "#A5D6A7",
        "Coffee Table": "#FFCC80",
        "Study Desk": "#80CBC4",
        "Dining Table": "#F48FB1",
        "Bookshelf": "#BCAAA4",
        "TV Unit": "#9FA8DA",
        "Bedside Table": "#CE93D8"
    }

    # DRAW FURNITURE
    for item in placements:

        if item["status"] != "Placed":
            continue

        x = item["x"]
        y = item["y"]
        width = item["width"]
        depth = item["depth"]

        color = furniture_colors.get(
            item["name"],
            "#C9B7E8"
        )

        fig.add_shape(
            type="rect",
            x0=x,
            y0=y,
            x1=x + width,
            y1=y + depth,
            line=dict(color="#49366F", width=2),
            fillcolor=color,
            opacity=0.9
        )

        # FURNITURE LABEL
        fig.add_annotation(
            x=x + width / 2,
            y=y + depth / 2,
            text=(
                f"<b>{item['name']}</b><br>"
                f"{width} × {depth} ft<br>"
                f"{item.get('rotation', 0)}°"
            ),
            showarrow=False,
            font=dict(size=10, color="#28243A"),
            align="center"
        )

    # CHART DESIGN
    fig.update_layout(
        title={
            "text": "RoomVision AI - Smart Furniture Layout",
            "x": 0.5,
            "xanchor": "center"
        },
        xaxis=dict(
            title="Room Width (feet)",
            range=[0, room_width + 1],
            dtick=1,
            showgrid=True,
            gridcolor="#E6E0EF",
            scaleanchor="y"
        ),
        yaxis=dict(
            title="Room Length (feet)",
            range=[0, room_length + 1],
            dtick=1,
            showgrid=True,
            gridcolor="#E6E0EF"
        ),
        height=700,
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False,
        margin=dict(l=70, r=80, t=100, b=70)
    )

  
    # DRAW DOORS AND WINDOWS
    
    # DRAW DOORS AND WINDOWS
    for opening in openings:

        x = opening["x"]
        y = opening["y"]

        opening_type = opening["type"].strip().lower()

        if opening_type == "door":
            color = "#FF6B00"
            label = "DOOR"

        elif opening_type == "window":
            color = "#0077FF"
            label = "WINDOW"

        else:
            continue

        fig.add_trace(
            go.Scatter(
                x=[x],
                y=[y],
                mode="markers+text",
                marker=dict(
                    size=28,
                    color=color,
                    symbol="diamond",
                    line=dict(
                        color="#28243A",
                        width=2
                    )
                ),
                text=[label],
                textposition="top center",
                textfont=dict(
                    size=14,
                    color=color
                ),
                showlegend=False,
                cliponaxis=False
            )
        )

    return fig
