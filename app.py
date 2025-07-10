import streamlit as st
import easyocr
from PIL import Image
import numpy as np

st.set_page_config(page_title="RecText 3.O", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

    html, body, .main, .block-container {
        font-family: 'Inter', sans-serif;
        background-color: #e6f2ff !important;
        color: #0f172a;
        margin: 0;
        padding: 0;
    }

    .main-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 2rem;
        background-color: white;
        border-radius: 16px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
    }

    h1.title {
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        color: #0f172a;
    }

    p.subtitle {
        text-align: center;
        font-size: 1rem;
        color: #555;
        margin-bottom: 2rem;
    }

    .stDownloadButton > button {
        background-color: #0ea5e9;
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 6px;
        padding: 0.6rem 1.2rem;
        margin-top: 10px;
        transition: 0.3s ease;
    }

    .stDownloadButton > button:hover {
        background-color: #0284c7;
    }
    </style>
""", unsafe_allow_html=True)

# Layout container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.markdown('<h1 class="title">📄 RecText 3.O</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Upload an image and extract text using EasyOCR</p>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    image_np = np.array(image)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🖼️ Preview")
        st.image(image, use_container_width=True)

    with col2:
        st.subheader("📝 Text Output")
        with st.spinner("Extracting text..."):
            reader = easyocr.Reader(['en'], gpu=False)
            results = reader.readtext(image_np)
            extracted_text = '\n'.join([text for _, text, _ in results])

        if extracted_text.strip():
            st.success("✅ Text extracted successfully!")
            st.text_area("Extracted Text", extracted_text, height=220)
            st.download_button("📥 Download Text", extracted_text, file_name="extracted_text.txt")
        else:
            st.error("❌ No text detected. Please try a clearer image.")

st.markdown('</div>', unsafe_allow_html=True)




