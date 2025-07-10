import streamlit as st
import easyocr
from PIL import Image
import numpy as np

st.set_page_config(page_title="RecText 3.O", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(to right, #e0eafc, #cfdef3);
    }

    .stApp {
        padding: 2rem;
    }

    .title {
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }

    .subtitle {
        text-align: center;
        color: #444;
        margin-bottom: 2rem;
        font-size: 1.1rem;
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

st.markdown('<div class="title">📄 RecText 3.O</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload an image to extract text using EasyOCR - open source.</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    image_np = np.array(image)

    col1, col2 = st.columns([1, 1]) 

    with col1:
        st.markdown("### 🖼️ Uploaded Image")
        st.image(image, caption="Preview", use_container_width=True)

    with col2:
        st.markdown("### 🔍 Extracted Text")
        with st.spinner("Extracting text..."):
            reader = easyocr.Reader(['en'])
            results = reader.readtext(image_np)
            extracted_text = '\n'.join([text for _, text, _ in results])

        if extracted_text.strip():
            st.success("✅ Text successfully extracted!")
            st.text_area("📝 Text Output", extracted_text, height=300)
            st.download_button(
                "📥 Download Text",
                extracted_text,
                file_name="extracted_text.txt",
                mime="text/plain"
            )
        else:
            st.error("❌ No text detected. Try a clearer image.")


