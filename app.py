
from collections import Counter
from io import BytesIO
from datetime import datetime
from pathlib import Path

import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px

from modules.room_analysis.image_processor import process_image
from modules.object_detection.furniture_detector import detect_furniture
from modules.style_recognition.style_classifier import analyze_room_style

from modules.color_analysis.color_palette import extract_color_palette
from modules.color_analysis.color_recommender import (
    recommend_color_theme,
    get_available_themes
)

from modules.furniture_recommendation.furniture_recommender import (
    recommend_furniture,
    get_available_room_types,
    get_available_styles
)

from modules.budget.budget_estimator import (
    calculate_budget,
    get_budget_categories
)

from modules.space_optimization.space_optimizer import (
    analyze_room_space,
    generate_furniture_layout,
    create_floor_plan
)

from modules.room_transformation.room_transformer import (
    transform_room
)

from modules.space_optimization.room_editor import create_room_editor


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="RoomVision AI",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>


/* ==========================================
   ROOMVISION AI — PROFESSIONAL UI THEME
   ========================================== */

:root {
    --primary: #6750A4;
    --primary-dark: #4F378B;
    --primary-light: #EEE9F8;
    --background: #F5F6FA;
    --surface: #FFFFFF;
    --text-main: #20283A;
    --text-secondary: #596579;
    --border: #E1E5ED;
    --sidebar: #192235;
}

/* MAIN APPLICATION */

.stApp {
    background-color: var(--background) !important;
    font-family: "Segoe UI", sans-serif;
    color: var(--text-main) !important;
}

[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background-color: var(--background) !important;
}

.block-container {
    padding: 2rem 3rem 3rem 3rem;
    max-width: 1450px;
}

/* GLOBAL TEXT VISIBILITY */

[data-testid="stMain"] p,
[data-testid="stMain"] li,
[data-testid="stMain"] span,
[data-testid="stMain"] label,
[data-testid="stMain"] small,
[data-testid="stMain"] div {
    color: inherit;
}

[data-testid="stMain"] {
    color: var(--text-main) !important;
}

[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stText"],
[data-testid="stCaptionContainer"] p {
    color: var(--text-secondary) !important;
    line-height: 1.65;
}

/* HEADINGS */

[data-testid="stMain"] h1,
[data-testid="stMain"] h2,
[data-testid="stMain"] h3,
[data-testid="stMain"] h4,
[data-testid="stMain"] h5 {
    color: var(--text-main) !important;
    font-weight: 700 !important;
}

[data-testid="stMain"] h1 {
    font-size: 2.1rem;
}

[data-testid="stMain"] h2 {
    font-size: 1.65rem;
}

[data-testid="stMain"] h3 {
    font-size: 1.25rem;
}

/* BOLD TEXT */

[data-testid="stMain"] strong,
[data-testid="stMain"] b {
    color: #252D40 !important;
    font-weight: 700 !important;
}

/* HERO SECTION */

.hero {
    background: linear-gradient(120deg, #252D48, #6750A4);
    padding: 42px;
    border-radius: 18px;
    margin-bottom: 30px;
    box-shadow: 0 8px 25px rgba(35, 39, 65, 0.12);
}

.hero h1 {
    color: #FFFFFF !important;
    font-size: 36px;
    font-weight: 750;
    margin-bottom: 12px;
}

.hero p {
    color: #F0ECFA !important;
    font-size: 16px;
    line-height: 1.8;
}

/* SECTION TITLES */

.section-title {
    color: var(--text-main) !important;
    font-size: 25px;
    font-weight: 700;
    margin: 30px 0 8px;
}

.section-description {
    color: var(--text-secondary) !important;
    font-size: 15px;
    margin-bottom: 20px;
}

/* FEATURE CARDS */

.feature-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 23px;
    min-height: 155px;
    box-shadow: 0 4px 15px rgba(25, 34, 53, 0.05);
}

.feature-icon {
    font-size: 30px;
    margin-bottom: 12px;
}

.feature-card h3 {
    color: var(--text-main) !important;
    font-size: 17px;
}

.feature-card p {
    color: var(--text-secondary) !important;
    font-size: 13px;
    line-height: 1.7;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background-color: var(--sidebar) !important;
    border-right: 1px solid #303B50;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span {
    color: #FFFFFF !important;
}

section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #C5CDE0 !important;
}

section[data-testid="stSidebar"] [data-testid="stRadio"] label {
    color: #FFFFFF !important;
}

section[data-testid="stSidebar"] [role="radiogroup"] label {
    background-color: transparent;
    border-radius: 8px;
}

/* INPUT LABELS */

[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label,
.stSelectbox label,
.stTextInput label,
.stNumberInput label,
.stMultiSelect label,
.stRadio label,
.stCheckbox label {
    color: var(--text-main) !important;
    font-weight: 600 !important;
}

/* TEXT INPUTS */

[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stTextArea"] textarea {
    background-color: #FFFFFF !important;
    color: var(--text-main) !important;
    border: 1px solid #C9CFDA !important;
    border-radius: 9px !important;
}

[data-testid="stTextInput"] input::placeholder,
[data-testid="stTextArea"] textarea::placeholder {
    color: #788397 !important;
}

/* DROPDOWNS */

div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border: 1px solid #C9CFDA !important;
    border-radius: 9px !important;
}

div[data-baseweb="select"] span {
    color: var(--text-main) !important;
}

[data-baseweb="popover"],
[data-baseweb="menu"],
[role="listbox"] {
    background-color: #FFFFFF !important;
}

[role="option"] {
    color: var(--text-main) !important;
}

/* BUTTONS */

.stButton button,
.stDownloadButton button {
    background: var(--primary) !important;
    color: #FFFFFF !important;
    border: 1px solid var(--primary) !important;
    border-radius: 9px !important;
    padding: 10px 22px;
    font-weight: 600 !important;
    transition: 0.2s ease;
}

.stButton button:hover,
.stDownloadButton button:hover {
    background: var(--primary-dark) !important;
    border-color: var(--primary-dark) !important;
    color: #FFFFFF !important;
}

.stButton button p,
.stDownloadButton button p {
    color: #FFFFFF !important;
}

/* METRIC CARDS */

[data-testid="stMetric"] {
    background: #FFFFFF !important;
    padding: 18px;
    border: 1px solid var(--border);
    border-radius: 13px;
    box-shadow: 0 3px 12px rgba(25, 34, 53, 0.04);
}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p {
    color: var(--text-secondary) !important;
}

[data-testid="stMetricValue"],
[data-testid="stMetricValue"] div {
    color: var(--text-main) !important;
    font-weight: 700 !important;
}

/* FILE UPLOADER */

[data-testid="stFileUploader"] {
    background: #FFFFFF;
    border: 1px dashed #B9A9D8;
    border-radius: 12px;
    padding: 12px;
}

[data-testid="stFileUploader"] label,
[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] section,
[data-testid="stFileUploader"] span {
    color: var(--text-main) !important;
}

/* DATAFRAMES AND TABLES */

[data-testid="stDataFrame"],
[data-testid="stTable"] {
    background: #FFFFFF !important;
    border-radius: 10px;
}

/* EXPANDERS */

[data-testid="stExpander"] {
    background: #FFFFFF !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary p {
    color: var(--text-main) !important;
    font-weight: 600 !important;
}

/* ALERTS */

[data-testid="stAlert"] {
    border-radius: 10px !important;
}

/* CAPTIONS */

[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p {
    color: var(--text-secondary) !important;
    font-size: 13px;
}

/* TABS */

button[data-baseweb="tab"] {
    color: var(--text-secondary) !important;
    font-weight: 600 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--primary) !important;
}

/* DIVIDERS */

hr {
    border-color: var(--border) !important;
}

/* LINKS */

[data-testid="stMain"] a {
    color: var(--primary-dark) !important;
    font-weight: 600;
}

/* SCROLLBAR */

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: #B8AECF;
    border-radius: 10px;
}

/* HIDE STREAMLIT BRANDING */

#MainMenu,
footer {
    visibility: hidden;
}


</style>
""", unsafe_allow_html=True)


# =====================================================
# SIDEBAR NAVIGATION
# =====================================================

st.sidebar.markdown("""
<h2 style='font-size:25px;'>🏡 RoomVision AI</h2>

<p style='color:#D4C5E9 !important; font-size:13px;'>
Your Intelligent Interior Designer
</p>
""", unsafe_allow_html=True)

st.sidebar.divider()

st.sidebar.markdown("### Navigation")

page = st.sidebar.radio(
    "Explore",
    [
        "Home",
        "Room Analysis",
        "AI Room Transformation",
        "Furniture Recommendations",
        "Budget Estimator",
        "Space Optimization"
    ],
    label_visibility="collapsed"
)

st.sidebar.divider()

st.sidebar.markdown("""
<p style='font-size:12px; color:#D4C5E9 !important;'>
AI-Powered Interior Design<br>
Version 1.0
</p>
""", unsafe_allow_html=True)


# =====================================================
# HOME PAGE
# =====================================================


def generate_design_recommendations(
    room_type,
    interior_style,
    color_theme
):

    recommendations = {

        "Wall Colors": {
            "Purple and White": "Lavender, soft white and muted lilac.",
            "Beige and Cream": "Warm beige, ivory and cream.",
            "White and Gold": "Pure white with subtle gold accents.",
            "Brown and Earthy": "Terracotta, warm brown and sand.",
            "Pastel": "Soft pink, mint and powder blue.",
            "Black and Grey": "Charcoal, light grey and white.",
            "Green and White": "Sage green, olive and soft white."
        },

        "Furniture": {
            "Modern": "Clean-lined furniture with simple finishes.",
            "Minimalist": "Functional furniture with uncluttered designs.",
            "Luxury": "Premium-looking furniture with elegant details.",
            "Traditional": "Classic wooden furniture with timeless designs.",
            "Scandinavian": "Light wooden furniture with simple shapes.",
            "Industrial": "Metal accents with wood and sturdy finishes.",
            "Bohemian": "Natural materials, woven textures and relaxed furniture."
        },

        "Lighting": {
            "Modern": "Recessed ceiling lights and pendant lighting.",
            "Minimalist": "Simple ceiling lights and soft task lighting.",
            "Luxury": "Decorative chandeliers and layered ambient lighting.",
            "Traditional": "Warm lamps and classic ceiling fixtures.",
            "Scandinavian": "Natural daylight and warm floor lamps.",
            "Industrial": "Metal pendant lights and exposed-style fixtures.",
            "Bohemian": "Warm lamps and decorative woven lighting."
        }
    }

    return {
        "Wall Color Suggestions":
            recommendations["Wall Colors"][color_theme],

        "Furniture Suggestions":
            recommendations["Furniture"][interior_style],

        "Lighting Suggestions":
            recommendations["Lighting"][interior_style],

        "Room Design Tip":
            f"Use a balanced furniture arrangement in your "
            f"{room_type.lower()} and maintain enough walking space."
    }
if page == "Home":

    st.markdown("""
    <div class="hero">
        <h1>Design Your Dream Space ✨</h1>
        <p>
        Welcome to RoomVision AI — your intelligent interior
        design assistant. Transform ordinary spaces into
        beautiful, personalized interiors using Artificial
        Intelligence.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-title">Explore Our AI Features</div>
    <div class="section-description">
    Everything you need to plan and transform your interiors.
    </div>
    """, unsafe_allow_html=True)

    features = [
        ("📸", "Room Analysis",
         "Analyze room photographs and identify existing furniture and objects."),
        ("🎨", "AI Transformation",
         "Explore beautiful room redesigns with AI-powered image generation."),
        ("🛋️", "Smart Recommendations",
         "Discover furniture matching your preferred design style."),
        ("💰", "Budget Estimator",
         "Estimate interior design expenses based on your budget."),
        ("📐", "Space Optimization",
         "Explore practical furniture arrangements for your room."),
        ("📊", "Design Reports",
         "View and download your interior design reports.")
    ]

    for row in range(2):

        columns = st.columns(3)

        for col, feature in zip(columns, features[row * 3:(row + 1) * 3]):

            with col:

                st.markdown(f"""
                <div class="feature-card">
                    <div class="feature-icon">{feature[0]}</div>
                    <h3>{feature[1]}</h3>
                    <p>{feature[2]}</p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("""
    <div class="section-title">How RoomVision AI Works</div>
    <div class="section-description">
        Transform your space in three simple steps.
    </div>
    """, unsafe_allow_html=True)

    workflow_steps = [
        (
            "📸",
            "1. Upload Your Room",
            "Upload a picture of your room to begin your interior design journey."
        ),
        (
            "🤖",
            "2. Analyze with AI",
            "Let AI analyze your room, identify furniture, colors and available space."
        ),
        (
            "✨",
            "3. Design & Optimize",
            "Explore creative room transformations, furniture ideas and smart layouts."
        )
    ]

    columns = st.columns(3)

    for col, step in zip(columns, workflow_steps):
        with col:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{step[0]}</div>
                <h3>{step[1]}</h3>
                <p>{step[2]}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #49366B, #8064A8);
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin-top: 25px;
        color: white;
    ">
        <h2 style="color: white;">Smarter Spaces. Better Living.</h2>
        <p style="color: white;">
            Discover the possibilities of AI-powered interior design
            with RoomVision AI.
        </p>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# ROOM ANALYSIS
# =====================================================

elif page == "Room Analysis":

    st.markdown("""
    <div class="hero">
        <h1>Room Analysis 📸</h1>
        <p>Upload your room photograph to begin intelligent analysis.</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_image = st.file_uploader(
        "Choose a room photograph",
        type=["jpg", "jpeg", "png"],
        key="analysis_upload"
    )

    if uploaded_image is not None:

        try:

            original_image = Image.open(
                uploaded_image
            ).convert("RGB")

            uploaded_image.seek(0)

            result = process_image(uploaded_image)

            file_size = uploaded_image.getbuffer().nbytes / 1024

            st.success("Image uploaded and processed successfully!")

            col1, col2 = st.columns(2)

            with col1:

                st.subheader("Original Room Image")

                st.image(
                    original_image,
                    width="stretch"
                )

            with col2:

                st.subheader("Processed Room Image")

                st.image(
                    result["image"],
                    width="stretch"
                )

            st.divider()

            # OBJECT DETECTION

            st.subheader("AI Furniture & Object Detection")

            with st.spinner("YOLO is analyzing your room..."):

                detection_result = detect_furniture(
                    result["image"]
                )

            detected_objects = detection_result["detected_objects"]

            if detected_objects:

                st.success(
                    f"Successfully detected {len(detected_objects)} objects!"
                )

                st.image(
                    detection_result["annotated_image"],
                    caption="AI-detected objects",
                    width="stretch"
                )

                furniture_items = [
                    "bed", "chair", "couch", "dining table"
                ]

                decor_items = [
                    "potted plant", "vase", "clock", "book"
                ]

                electronics_items = [
                    "tv", "laptop", "mouse", "remote",
                    "keyboard", "cell phone"
                ]

                def categorize_object(name):

                    if name in furniture_items:
                        return "Furniture"

                    elif name in decor_items:
                        return "Decor"

                    elif name in electronics_items:
                        return "Electronics"

                    return "Other"

                for obj in detected_objects:
                    obj["category"] = categorize_object(obj["name"])

                # STYLE RECOGNITION

                st.divider()
                st.subheader("🎨 AI Room Style Recognition")

                style_result = analyze_room_style(result["image"])

                st.success(
                    f"Predicted Interior Style: {style_result['style']}"
                )

                st.metric(
                    "Relative Style Score",
                    f"{style_result['confidence']}%"
                )

                st.dataframe(
                    [
                        {
                            "Interior Style": style,
                            "Score": score
                        }
                        for style, score in style_result["all_scores"].items()
                    ],
                    use_container_width=True,
                    hide_index=True
                )

                # COLOR PALETTE

                st.divider()
                st.subheader("🎨 AI Color Palette Generator")

                color_palette = extract_color_palette(
                    result["image"],
                    num_colors=6
                )

                palette_columns = st.columns(6)

                for index, color in enumerate(color_palette):

                    with palette_columns[index]:

                        st.markdown(
                            f"""
                            <div style="
                                background-color: {color['hex']};
                                height: 85px;
                                border-radius: 12px;
                                border: 1px solid #cccccc;
                            "></div>
                            """,
                            unsafe_allow_html=True
                        )

                        st.caption(color["hex"])
                        st.caption(f"{color['percentage']}%")

                st.dataframe(
                    [
                        {
                            "HEX Code": color["hex"],
                            "RGB": str(color["rgb"]),
                            "Percentage": f"{color['percentage']}%"
                        }
                        for color in color_palette
                    ],
                    use_container_width=True,
                    hide_index=True
                )

                # COLOR RECOMMENDATIONS

                st.divider()
                st.subheader("🏡 Smart Interior Color Recommendations")

                selected_theme = st.selectbox(
                    "Choose Your Interior Color Theme",
                    get_available_themes(),
                    key="room_color_theme"
                )

                theme_result = recommend_color_theme(selected_theme)

                st.write(
                    f"Recommended colors for {selected_theme}:"
                )

                theme_columns = st.columns(5)

                for index, (name, hex_code) in enumerate(
                    theme_result["colors"].items()
                ):

                    with theme_columns[index]:

                        st.markdown(
                            f"""
                            <div style="
                                background-color: {hex_code};
                                height: 90px;
                                border-radius: 12px;
                                border: 1px solid #cccccc;
                            "></div>
                            """,
                            unsafe_allow_html=True
                        )

                        st.caption(name)
                        st.caption(hex_code)

                # DETECTION SUMMARY

                st.divider()
                st.subheader("Detection Summary")

                object_counts = Counter(
                    obj["name"] for obj in detected_objects
                )

                category_counts = Counter(
                    obj["category"] for obj in detected_objects
                )

                total_objects = len(detected_objects)

                average_confidence = sum(
                    obj["confidence"] for obj in detected_objects
                ) / total_objects

                c1, c2, c3 = st.columns(3)

                c1.metric("Total Objects", total_objects)

                c2.metric("Object Types", len(object_counts))

                c3.metric(
                    "Average Confidence",
                    f"{average_confidence:.2f}%"
                )

                st.subheader("Object Category Summary")

                st.dataframe(
                    [
                        {
                            "Category": category,
                            "Quantity": count
                        }
                        for category, count in category_counts.items()
                    ],
                    use_container_width=True,
                    hide_index=True
                )

                st.subheader("Furniture & Object Counts")

                st.dataframe(
                    [
                        {
                            "Object": name.replace("_", " ").title(),
                            "Category": categorize_object(name),
                            "Quantity": count
                        }
                        for name, count in object_counts.items()
                    ],
                    use_container_width=True,
                    hide_index=True
                )

                st.subheader("Individual Detection Results")

                st.dataframe(
                    [
                        {
                            "Object": obj["name"].replace("_", " ").title(),
                            "Category": obj["category"],
                            "Confidence": f'{obj["confidence"]:.2f}%'
                        }
                        for obj in detected_objects
                    ],
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.warning(
                    "No objects detected. Try another room photograph."
                )

            # IMAGE INFORMATION

            st.divider()
            st.subheader("Original Image Information")

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Original Width",
                f'{result["original_width"]} px'
            )

            c2.metric(
                "Original Height",
                f'{result["original_height"]} px'
            )

            c3.metric(
                "Image Format",
                str(result["format"])
            )

            st.subheader("Processed Image Information")

            c4, c5, c6 = st.columns(3)

            c4.metric(
                "Processed Width",
                f'{result["processed_width"]} px'
            )

            c5.metric(
                "Processed Height",
                f'{result["processed_height"]} px'
            )

            c6.metric(
                "File Size",
                f"{file_size:.2f} KB"
            )

            st.success("Room analysis completed!")

        except Exception as e:

            st.error(f"Room analysis failed: {e}")
            st.exception(e)

    else:

        st.info("Please upload a room photograph to begin.")


# =====================================================
#
# =====================================================
# AI ROOM TRANSFORMATION
# =====================================================

elif page == "AI Room Transformation":

    st.markdown("""
    <div class="hero">
        <h1>🎨 AI Room Transformation</h1>
        <p>
        Create your dream interior from a simple description
        using AI-powered image generation.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 1. CHOOSE ROOM
    st.subheader("1. Choose Your Room")

    transformation_room_type = st.selectbox(
        "Select Room Type",
        ["Bedroom", "Living Room", "Kitchen", "Dining Room", "Study Room"],
        key="transformation_room_type"
    )

    st.divider()

    # 2. CUSTOMIZE INTERIOR
    st.subheader("2. Customize Your Interior")

    col1, col2 = st.columns(2)

    with col1:
        transformation_style = st.selectbox(
            "Select Interior Design Style",
            ["Modern", "Minimalist", "Luxury", "Traditional", "Scandinavian", "Industrial", "Bohemian"],
            key="transformation_style"
        )

        transformation_color = st.selectbox(
            "Select Color Theme",
            ["Purple and White", "Beige and Cream", "White and Gold", "Brown and Earthy", "Pastel", "Black and Grey", "Green and White"],
            key="transformation_color"
        )

    with col2:
        custom_instructions = st.text_area(
            "Additional Design Instructions",
            placeholder=(
                "Example: Create a beautiful bedroom with a king-size bed, "
                "wardrobe, study table, purple curtains and warm lighting."
            ),
            key="transformation_instructions"
        )

    st.divider()

    # 3. GENERATE NEW INTERIOR
    st.subheader("3. Generate Your New Interior")

    if st.button(
        "✨ Generate My Dream Room",
        type="primary",
        key="generate_transformation"
    ):
        try:
            account_id = st.secrets["CLOUDFLARE_ACCOUNT_ID"]
            api_token = st.secrets["CLOUDFLARE_API_TOKEN"]

            with st.spinner("Creating your dream interior... Please wait."):
                generated_image = transform_room(
                    room_type=transformation_room_type,
                    interior_style=transformation_style,
                    color_theme=transformation_color,
                    account_id=account_id,
                    api_token=api_token,
                    custom_instructions=custom_instructions
                )

            if generated_image is not None:
                st.session_state["transformed_room_image"] = generated_image

                history_folder = Path(__file__).resolve().parent / "generated_designs"
                history_folder.mkdir(parents=True, exist_ok=True)

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                filename = (
                    f"{timestamp}_{transformation_room_type}_"
                    f"{transformation_style}.png"
                )
                save_path = history_folder / filename
                generated_image.save(save_path)

                st.success("Your new interior has been generated successfully!")
            else:
                st.error("The AI service returned no image.")

        except Exception as e:
            error_message = str(e).lower()

            if "429" in error_message or "limit" in error_message:
                st.warning(
                    "AI generation limit reached. Please try again later "
                    "or check your provider's current usage allowance."
                )
            elif "401" in error_message or "403" in error_message:
                st.error(
                    "Cloudflare authentication failed. Please check your API token and permissions."
                )
            elif "402" in error_message:
                st.error(
                    "The AI service reports that paid usage is required. "
                    "Please check your Cloudflare account and usage settings."
                )
            else:
                st.error(f"Unable to generate your room: {e}")

    # 4. DISPLAY MOST RECENT GENERATED IMAGE
    if "transformed_room_image" in st.session_state:
        st.divider()
        st.subheader("4. Your AI-Generated Interior")

        generated_image = st.session_state["transformed_room_image"]
        st.image(
            generated_image,
            caption="Your AI-Generated Dream Interior",
            width="stretch"
        )

        image_buffer = BytesIO()
        generated_image.save(image_buffer, format="PNG")

        st.download_button(
            label="⬇️ Download Your Dream Room",
            data=image_buffer.getvalue(),
            file_name="roomvision_dream_room.png",
            mime="image/png",
            key="download_latest_design"
        )

        st.caption(
            "AI-generated interior design is a visual suggestion. "
            "Check actual room dimensions before implementing it."
        )

    # 5. DESIGN HISTORY
    st.divider()
    st.subheader("📚 5. Your Design History")

    history_folder = Path(__file__).resolve().parent / "generated_designs"
    history_folder.mkdir(parents=True, exist_ok=True)

    history_images = sorted(
        history_folder.glob("*.png"),
        key=lambda file: file.stat().st_mtime,
        reverse=True
    )

    if history_images:
        st.write(f"You have generated {len(history_images)} designs.")
        columns = st.columns(2)

        for index, image_path in enumerate(history_images):
            with columns[index % 2]:
                with Image.open(image_path) as history_image:
                    st.image(
                        history_image.copy(),
                        caption=image_path.stem,
                        width="stretch"
                    )

                st.download_button(
                    label="⬇️ Download Design",
                    data=image_path.read_bytes(),
                    file_name=image_path.name,
                    mime="image/png",
                    key=f"history_download_{image_path.name}"
                )
    else:
        st.info(
            "Your design history is empty. Generate your first room design!"
        )

    # 6. COMPARE ROOM DESIGNS
    st.divider()
    st.subheader("🆚 6. Compare Your Room Designs")

    if len(history_images) >= 2:
        design_names = [image_path.name for image_path in history_images]

        selected_designs = st.multiselect(
            "Select two designs to compare:",
            options=design_names,
            max_selections=2,
            key="compare_designs"
        )

        if len(selected_designs) == 2:
            st.write("### Your Design Comparison")
            col1, col2 = st.columns(2)

            design1_path = history_folder / selected_designs[0]
            design2_path = history_folder / selected_designs[1]

            with col1:
                with Image.open(design1_path) as design1:
                    st.image(
                        design1.copy(),
                        caption=f"Design 1: {design1_path.stem}",
                        width="stretch"
                    )

            with col2:
                with Image.open(design2_path) as design2:
                    st.image(
                        design2.copy(),
                        caption=f"Design 2: {design2_path.stem}",
                        width="stretch"
                    )
    else:
        st.info(
            "Generate at least two room designs to use the comparison feature."
        )

    # 7. AI DESIGN RECOMMENDATIONS
    st.divider()
    st.subheader("✨ 7. AI Design Recommendations")
    st.write(
        "Get personalized interior design suggestions for your dream room."
    )

    recommendation_room = st.selectbox(
        "Choose your room:",
        ["Bedroom", "Living Room", "Kitchen", "Dining Room", "Study Room"],
        key="recommendation_room"
    )

    recommendation_style = st.selectbox(
        "Choose your preferred style:",
        ["Modern", "Minimalist", "Luxury", "Traditional", "Scandinavian", "Industrial", "Bohemian"],
        key="recommendation_style"
    )

    recommendation_color = st.selectbox(
        "Choose your color theme:",
        ["Purple and White", "Beige and Cream", "White and Gold", "Brown and Earthy", "Pastel", "Black and Grey", "Green and White"],
        key="recommendation_color"
    )

    if st.button(
        "✨ Get Design Recommendations",
        type="primary",
        key="get_recommendations"
    ):
        design_recommendations = generate_design_recommendations(
            room_type=recommendation_room,
            interior_style=recommendation_style,
            color_theme=recommendation_color
        )

        st.success("Your design recommendations are ready!")

        for title, suggestion in design_recommendations.items():
            st.markdown(f"### {title}")
            st.write(suggestion)


# =====================================================
# FURNITURE RECOMMENDATIONS
# =====================================================

elif page == "Furniture Recommendations":

    st.markdown("""
    <div class="hero">
        <h1>Smart Furniture Recommendations 🛋️</h1>
        <p>Discover furniture matching your room, style and budget.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        selected_room = st.selectbox(
            "Select Room Type",
            get_available_room_types()
        )

        selected_style = st.selectbox(
            "Select Interior Style",
            get_available_styles()
        )

    with col2:

        furniture_budget = st.number_input(
            "Maximum budget per item (₹)",
            min_value=1000,
            max_value=500000,
            value=20000,
            step=1000
        )

        selected_categories = st.multiselect(
            "Furniture Categories",
            [
                "Bed",
                "Storage",
                "Table",
                "Seating",
                "Workspace"
            ],
            default=[
                "Bed",
                "Storage",
                "Table",
                "Seating",
                "Workspace"
            ]
        )

    if st.button(
        "Find Furniture Recommendations",
        type="primary"
    ):

        recommendations = recommend_furniture(
            room_type=selected_room,
            interior_style=selected_style,
            budget=furniture_budget,
            categories=selected_categories
        )

        st.divider()
        st.subheader("Your Furniture Recommendations")

        if recommendations:

            st.success(
                f"Found {len(recommendations)} matching furniture items!"
            )

            for item in recommendations:

                with st.container(border=True):

                    st.subheader(item["name"])

                    st.write(item["description"])

                    st.write(
                        f"**Category:** {item['category']}"
                    )

                    st.write(
                        f"**Estimated Price:** ₹{item['price']:,}"
                    )

                    st.caption(
                        "Compatible styles: " +
                        ", ".join(item["style"])
                    )

        else:

            st.warning(
                "No matching furniture found. "
                "Try changing your style, budget or categories."
            )

        st.caption(
            "Prices are illustrative estimates, not live market prices."
        )


# =====================================================
# BUDGET ESTIMATOR
# =====================================================

elif page == "Budget Estimator":

    st.markdown("""
    <div class="hero">
        <h1>💰 Advanced Budget Estimator</h1>
        <p>
        Plan your interior design expenses with intelligent cost estimation.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("1. Room Information")

    room_area = st.number_input(
        "Room Area (Square Feet)",
        min_value=1,
        max_value=10000,
        value=120,
        step=10
    )

    st.divider()

    st.subheader("2. Select Items and Quantities")

    budget_categories = get_budget_categories()

    selected_items = {}

    for category, items in budget_categories.items():

        with st.expander(
            f"🛋️ {category}",
            expanded=True
        ):

            category_items = {}

            for item_name, rate in items.items():

                col1, col2 = st.columns([3, 1])

                with col1:

                    st.write(f"**{item_name}**")
                    st.caption(f"Rate: ₹{rate:,}")

                with col2:

                    quantity = st.number_input(
                        "Quantity",
                        min_value=0,
                        max_value=100,
                        value=0,
                        step=1,
                        key=f"budget_{category}_{item_name}"
                    )

                if quantity > 0:

                    category_items[item_name] = quantity

            if category_items:

                selected_items[category] = category_items

    st.divider()

    if st.button(
        "Calculate My Interior Budget",
        type="primary"
    ):

        if not selected_items:

            st.warning("Please select at least one item.")

        else:

            budget_result = calculate_budget(
                selected_items,
                room_area
            )

            st.subheader("3. Your Estimated Budget")

            st.metric(
                "Total Estimated Cost",
                f"₹{budget_result['grand_total']:,}"
            )

            st.write(f"**Room Area:** {room_area} sq. ft.")

            st.divider()

            # COST BREAKDOWN

            st.subheader("Cost Breakdown")

            breakdown_rows = []

            for item_name, details in budget_result["breakdown"].items():

                breakdown_rows.append({
                    "Category": details["category"],
                    "Item": item_name,
                    "Rate (₹)": details["rate"],
                    "Quantity": details["quantity"],
                    "Total Cost (₹)": details["amount"]
                })

            breakdown_df = pd.DataFrame(breakdown_rows)

            st.dataframe(
                breakdown_df,
                use_container_width=True,
                hide_index=True
            )

            st.divider()

            # CATEGORY EXPENSES

            st.subheader("Category-wise Expenses")

            category_totals = (
                breakdown_df
                .groupby("Category", as_index=False)["Total Cost (₹)"]
                .sum()
                .sort_values(
                    "Total Cost (₹)",
                    ascending=False
                )
            )

            fig = px.pie(
                category_totals,
                names="Category",
                values="Total Cost (₹)",
                hole=0.55,
                title="Interior Budget Distribution",
                color_discrete_sequence=px.colors.qualitative.Pastel,
                hover_data={"Total Cost (₹)": ":,.0f"}
            )

            fig.update_traces(
                textposition="outside",
                textinfo="label+percent",
                textfont_size=13,
                marker=dict(
                    line=dict(color="white", width=2)
                )
            )

            fig.update_layout(
                height=450,
                showlegend=True,
                legend_title_text="Expense Categories",
                margin=dict(t=70, b=40, l=30, r=30),
                annotations=[
                    dict(
                        text=f"₹{budget_result['grand_total']:,}",
                        x=0.5,
                        y=0.5,
                        font_size=22,
                        showarrow=False
                    )
                ]
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.divider()

            # DOWNLOAD REPORT

            csv_data = breakdown_df.to_csv(index=False)

            st.download_button(
                label="Download Budget Report (CSV)",
                data=csv_data,
                file_name="roomvision_budget_report.csv",
                mime="text/csv"
            )

            st.caption(
                "Note: These are illustrative estimates. "
                "Actual costs depend on measurements, materials, "
                "labor and location."
            )


# =====================================================
# SPACE OPTIMIZATION
# =====================================================

elif page == "Space Optimization":

    st.markdown("""
    <div class="hero">
        <h1>📐 AI Space Optimization</h1>
        <p>Plan furniture placement and visualize your room layout.</p>
    </div>
    """, unsafe_allow_html=True)

    # ROOM DIMENSIONS

    st.subheader("1. Enter Room Dimensions")

    col1, col2 = st.columns(2)

    with col1:

        room_width = st.number_input(
            "Room Width (feet)",
            min_value=4.0,
            max_value=100.0,
            value=12.0,
            step=0.5
        )

    with col2:

        room_length = st.number_input(
            "Room Length (feet)",
            min_value=4.0,
            max_value=100.0,
            value=14.0,
            step=0.5
        )

    st.divider()

    # DOORS AND WINDOWS

    st.subheader("2. Mark Doors and Windows")

    if "room_openings" not in st.session_state:

        st.session_state.room_openings = []

    opening_type = st.radio(
        "Select what you want to mark",
        ["Door", "Window"],
        horizontal=True
    )

    st.caption(
        "Click close to any room wall to mark the selected opening."
    )

    clicked_points = create_room_editor(
        room_width,
        room_length,
        st.session_state.room_openings,
        opening_type
    )

    if clicked_points:

        clicked = clicked_points[-1]

        click_x = float(clicked["x"])
        click_y = float(clicked["y"])

        distances = {
            "Left": abs(click_x),
            "Right": abs(room_width - click_x),
            "Bottom": abs(click_y),
            "Top": abs(room_length - click_y)
        }

        wall = min(distances, key=distances.get)

        wall_distance = distances[wall]

        if wall_distance <= 0.5:

            if not any(
                abs(item["x"] - click_x) < 0.5
                and abs(item["y"] - click_y) < 0.5
                and item["type"] == opening_type
                for item in st.session_state.room_openings
            ):

                st.session_state.room_openings.append({
                    "type": opening_type,
                    "wall": wall,
                    "x": round(click_x, 2),
                    "y": round(click_y, 2)
                })

                st.success(
                    f"{opening_type} marked on {wall} wall!"
                )

                st.rerun()

        else:

            st.warning(
                "Please click closer to a room wall."
            )

    if st.session_state.room_openings:

        st.write("**Marked openings:**")

        st.dataframe(
            st.session_state.room_openings,
            use_container_width=True,
            hide_index=True
        )

        if st.button("Clear All Doors and Windows"):

            st.session_state.room_openings = []

            st.rerun()

    st.divider()

    # FURNITURE SELECTION

    st.subheader("3. Select Furniture")

    available_furniture = [
        "Bed",
        "Wardrobe",
        "Sofa",
        "Coffee Table",
        "Study Desk",
        "Dining Table",
        "Bookshelf",
        "TV Unit",
        "Bedside Table"
    ]

    selected_furniture = st.multiselect(
        "Choose furniture for your room",
        available_furniture,
        default=[
            "Bed",
            "Wardrobe",
            "Bedside Table"
        ]
    )

    st.divider()

    # OPTIMIZATION

    if st.button(
        "Optimize My Room",
        type="primary"
    ):

        if not selected_furniture:

            st.warning(
                "Please select at least one furniture item."
            )

        else:

            # ROOM SPACE ANALYSIS

            analysis = analyze_room_space(
                room_width,
                room_length,
                selected_furniture
            )

            st.subheader("4. Room Space Analysis")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Room Area",
                f"{analysis['room_area']} sq. ft."
            )

            col2.metric(
                "Occupied Area",
                f"{analysis['occupied_area']} sq. ft."
            )

            col3.metric(
                "Available Area",
                f"{analysis['available_area']} sq. ft."
            )

            st.metric(
                "Furniture Space Usage",
                f"{analysis['utilization_percentage']}%"
            )

            if analysis["warning"]:

                st.warning(analysis["warning"])

            st.info(analysis["recommendation"])

            st.divider()

            # FURNITURE PLACEMENT

            st.subheader("5. Furniture Placement Results")

            placements = generate_furniture_layout(
                room_width,
                room_length,
                selected_furniture
            )

            st.dataframe(
                placements,
                use_container_width=True,
                hide_index=True
            )

            st.divider()

            # FLOOR PLAN

            st.subheader("6. Interactive 2D Floor Plan")

            floor_plan = create_floor_plan(
                room_width,
                room_length,
                placements,
                st.session_state.room_openings
            )

            st.plotly_chart(
                floor_plan,
                use_container_width=True
            )

            st.caption(
                "Furniture dimensions and placement coordinates are "
                "approximate planning estimates. Verify measurements "
                "and walking clearances before arranging real furniture."
            )


# =====================================================
# FALLBACK PAGE
# =====================================================

else:

    st.markdown("""
    <div class="hero">
        <h1>RoomVision AI</h1>
        <p>Your intelligent interior design workspace.</p>
    </div>
    """, unsafe_allow_html=True)

    st.info("Select a feature from the navigation sidebar.")
