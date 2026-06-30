import streamlit as st
from PIL import Image
import time
import random
import requests

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AgriVision - Plant Identifier",
    page_icon="🌾",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #f0f7ec 0%, #ffffff 100%);
    }
    h1 {
        color: #2e7d32;
        text-align: center;
        font-weight: 700;
    }
    .subtitle {
        text-align: center;
        color: #558b2f;
        font-size: 18px;
        margin-bottom: 30px;
    }
    .result-card {
        background-color: #ffffff;
        border: 1px solid #c8e6c9;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(46, 125, 50, 0.08);
        margin-top: 20px;
    }
    .stButton>button {
        background-color: #2e7d32;
        color: white;
        border-radius: 8px;
        padding: 10px 24px;
        border: none;
        font-weight: 600;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #1b5e20;
        color: white;
    }
    [data-testid="stSidebar"] {
        background-color: #e8f5e9;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## 🌱 About")
    st.write(
        "Upload an image of a crop, leaf, or plant and this app will "
        "predict its name along with a confidence score."
    )
    st.markdown("---")
    st.markdown("### How it works")
    st.write("1. Upload an image (JPG/PNG)\n2. Click Predict\n3. View the result")
    st.markdown("---")
    st.caption("Built with Streamlit 🌾")

# ---------------- HEADER ----------------
st.title("🌾 AgriVision")
st.markdown('<p class="subtitle">Upload a crop or plant image to identify it</p>', unsafe_allow_html=True)

# ---------------- FILE UPLOADER ----------------
uploaded_file = st.file_uploader(
    "Drag and drop or browse an image",
    type=["jpg", "jpeg", "png"],
    help="Supported formats: JPG, JPEG, PNG"
)

# ---------------- My Work only on ----------------
ngrok_url="https://unfounded-tattle-pox.ngrok-free.dev"

# ---------------- MAIN LOGIC ----------------
if uploaded_file is not None:
    st.image(uploaded_file)
    file={
      "image":uploaded_file
    }

    if st.button("🔍 Predict"):
        with st.spinner("Analyzing image..."):
            response = requests.post(f"{ngrok_url}/predict", files=file)

        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        st.subheader("Result:")
        with col1:
            st.metric(label="Predicted Name", value=response.json()["predicted_class"])
        with col2:
            st.metric(label="Confidence", value=f"{response.json()["confidence"]*100:.2f}%")
        st.progress(response.json()["confidence"])
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("👆 Upload an image to get started.")