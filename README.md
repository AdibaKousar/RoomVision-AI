# 🏡 RoomVision AI

### AI-Powered Interior Design & Room Transformation Platform

RoomVision AI is an intelligent interior design application developed using Python and Streamlit. It helps users analyze their rooms, generate AI-powered interior designs, explore furniture recommendations, estimate budgets, and optimize available space.

## ✨ Features

### 📸 Room Analysis
- Upload and analyze room images.
- Identify furniture and objects.
- Extract room color information.
- Recognize interior design styles.

### 🎨 AI Room Transformation
- Generate creative interior designs using AI.
- Explore different interior styles and color themes.
- Generate personalized room design concepts.

### 🛋️ Furniture Recommendations
- Explore furniture suggestions.
- Discover suitable furniture based on room requirements.

### 💰 Budget Estimator
- Estimate interior design expenses.
- Plan furniture and decoration budgets.

### 📐 Space Optimization
- Visualize furniture arrangements.
- Generate 2D room floor plans.
- Explore practical space utilization.

### 📊 Design Reports
- View design information.
- Generate and download reports.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming |
| Streamlit | Web application |
| OpenCV | Image processing |
| Pillow | Image manipulation |
| NumPy | Numerical operations |
| Pandas | Data processing |
| Plotly | Interactive visualizations |
| Cloudflare Workers AI | AI image generation |

## 📂 Project Structure

```text
RoomVision-AI/
│
├── app.py
├── modules/
│   ├── room_analysis/
│   ├── object_detection/
│   ├── style_recognition/
│   ├── color_analysis/
│   ├── room_transformation/
│   └── ...
│
├── pages/
├── assets/
├── .streamlit/
├── .gitignore
├── requirements.txt
└── README.md
```

*Note: Update the illustrative folder structure to match your actual project.*

## 🚀 Installation & Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the project folder

```bash
cd RoomVision-AI
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

Windows:

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure API credentials

Create a local `.streamlit/secrets.toml` file and configure the required Cloudflare credentials.

Never upload API tokens, passwords, or private credentials to GitHub.

### 7. Run the application

```bash
streamlit run app.py
```

## 🎯 Project Objective

To make interior design more accessible through artificial intelligence by providing room analysis, creative design generation, furniture recommendations, budget planning, and intelligent space optimization.

## 👩‍💻 Developed By

**Adiba Kousar**

AI & Data Science Student

## 💜 Project

**RoomVision AI — Smarter Spaces. Better Living.**