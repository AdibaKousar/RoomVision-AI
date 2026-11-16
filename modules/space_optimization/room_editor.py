
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events


def create_room_editor(
    room_width,
    room_length,
    openings=None,
    opening_type="Door"
):
    if openings is None:
        openings = []

    fig = go.Figure()

    # Room boundary
    fig.add_shape(
        type="rect",
        x0=0, y0=0,
        x1=room_width, y1=room_length,
        line=dict(color="#49366F", width=5),
        fillcolor="#F7F4FC"
    )

    # Four wall click targets
    fig.add_trace(
        go.Scatter(
            x=[room_width / 2, room_width / 2, 0, room_width],
            y=[0, room_length, room_length / 2, room_length / 2],
            mode="markers+text",
            marker=dict(size=25, color="#8064A2"),
            text=["BOTTOM", "TOP", "LEFT", "RIGHT"],
            textposition="top center",
            customdata=["Bottom", "Top", "Left", "Right"],
            hoverinfo="text"
        )
    )

    # Existing openings
    for opening in openings:
        fig.add_trace(
            go.Scatter(
                x=[opening["x"]],
                y=[opening["y"]],
                mode="markers+text",
                marker=dict(
                    size=18,
                    color="#D97706" if opening["type"] == "Door" else "#0284C7"
                ),
                text=[opening["type"]],
                textposition="top center"
            )
        )

    fig.update_layout(
        title=f"Click a wall marker to place a {opening_type}",
        xaxis=dict(
            range=[-1, room_width + 1],
            title="Room Width (feet)",
            scaleanchor="y"
        ),
        yaxis=dict(
            range=[-1, room_length + 1],
            title="Room Length (feet)"
        ),
        height=600
    )

    clicked_points = plotly_events(
        fig,
        click_event=True,
        select_event=False,
        hover_event=False,
        override_height=600,
        key="room_wall_clicks"
    )

    return clicked_points
