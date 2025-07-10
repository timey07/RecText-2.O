import streamlit as st
import easyocr
from PIL import Image
import numpy as np

st.set_page_config(page_title="RecText 3.O", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

    html, body, .appview-container .main, .block-container {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(to right, #cce5ff, #e6f2ff) !important;
        color: #0f172a !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    .main-container {
        max-width: 850px;
        margin: 40px auto;
        padding: 30px;
        background: rgba(255, 255, 255, 0.97);
        border-radius: 20px;
        box-shadow: 0 6px 25px rgba(0, 0, 0, 0.1);
    }

    .title {
        font-size: 2.4rem;
        text-align: center;
        color: #0f172a;
        margin-bottom: 0.3rem;
    }

    .subtitle {
        text-align: center;
        font-size: 1rem;
        color: #475569;
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

    .element-container:has(iframe) {
        display: none !important;
    }

    /* Remove top padding that causes white bar */
    .block-container {
        padding-top: 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Main container
with st.container():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<div class="title">📄 RecText 3.O</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Upload an image and extract text using EasyOCR</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        image_np = np.array(image)

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("##### 🖼️ Preview")
            st.image(image, use_container_width=True)

        with col2:
            st.markdown("##### 📝 Text Output")
            with st.spinner("Extracting..."):
                reader = easyocr.Reader(['en'], gpu=False)
                results = reader.readtext(image_np)
                extracted_text = '\n'.join([text for _, text, _ in results])

            if extracted_text.strip():
                st.success("✅ Done")
                st.text_area("Extracted Text", extracted_text, height=220)
                st.download_button("📥 Download Text", extracted_text, file_name="text.txt")
            else:
                st.error("❌ No text detected. Please upload a clearer image.")

    st.markdown('</div>', unsafe_allow_html=True)



