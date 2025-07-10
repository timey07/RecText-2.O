import streamlit as st
import easyocr
from PIL import Image
import numpy as np

st.set_page_config(page_title="RecText 3.O", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background: #f0f4f8;
    }

    .main-container {
        max-width: 950px;
        margin: auto;
        padding: 2rem;
        background: white;
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    }

    .title {
        font-size: 2rem;
        text-align: center;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1rem;
        margin-bottom: 2rem;
    }

    .stDownloadButton > button {
        background-color: #10b981;
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 6px;
        padding: 0.6rem 1.2rem;
    }

    .stDownloadButton > button:hover {
        background-color: #059669;
    }
    </style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<div class="title">📄 RecText 3.O</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Upload an image to extract readable text using AI</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        image_np = np.array(image)

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("##### 🖼️ Uploaded Image")
            st.image(image, use_container_width=True)

        with col2:
            st.markdown("##### 🔍 Extracted Text")
            with st.spinner("Extracting text..."):
                reader = easyocr.Reader(['en'])
                results = reader.readtext(image_np)
                extracted_text = '\n'.join([text for _, text, _ in results])

            if extracted_text.strip():
                st.success("✅ Text extracted successfully!")
                st.text_area("Text Output", extracted_text, height=300)
                st.download_button("📥 Download Text", extracted_text, file_name="extracted_text.txt")
            else:
                st.error("❌ No text detected. Try a clearer image.")

    st.markdown('</div>', unsafe_allow_html=True)

