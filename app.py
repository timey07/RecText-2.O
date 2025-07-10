import streamlit as st
import easyocr
from PIL import Image
import numpy as np

st.set_page_config(page_title="RecText 3.O", layout="centered")

# Custom CSS for layout, font, and animated background
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        margin: 0 !important;
        padding: 0 !important;
        background: url('https://www.transparenttextures.com/patterns/white-wall-3.png'), 
                    linear-gradient(to right, #e0eafc, #cfdef3);
        background-size: cover;
        background-repeat: repeat;
    }

    .main-container {
        max-width: 850px;
        margin: 30px auto 0 auto;
        padding: 30px 30px 20px 30px;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        box-shadow: 0 6px 25px rgba(0,0,0,0.1);
    }

    .title {
        font-size: 2.2rem;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }

    .stDownloadButton > button {
        background-color: #10b981;
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        margin-top: 10px;
    }

    .stDownloadButton > button:hover {
        background-color: #059669;
    }

    .element-container:has(iframe) {
        display: none !important;
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
                reader = easyocr.Reader(['en'])
                results = reader.readtext(image_np)
                extracted_text = '\n'.join([text for _, text, _ in results])

            if extracted_text.strip():
                st.success("✅ Done")
                st.text_area("Extracted Text", extracted_text, height=220)
                st.download_button("📥 Download Text", extracted_text, file_name="text.txt")
            else:
                st.error("❌ No text detected. Please upload a clearer image.")

    st.markdown('</div>', unsafe_allow_html=True)


