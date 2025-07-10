import streamlit as st
import easyocr
from PIL import Image
import numpy as np

st.set_page_config(page_title="RecText 3.0", page_icon="📄", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(to right, #e0eafc, #cfdef3);
}

#MainMenu, footer, header { visibility: hidden; }

.container {
    background: #ffffffcc;
    padding: 2rem;
    border-radius: 20px;
    max-width: 850px;
    margin: 2rem auto;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
}

.title {
    text-align: center;
    font-size: 2.2rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.subtitle {
    text-align: center;
    color: #555;
    font-size: 1rem;
    margin-bottom: 1.5rem;
}

.stat-box {
    text-align: center;
    background: #f8fafc;
    padding: 0.8rem;
    border-radius: 10px;
}

.stat-number {
    font-size: 1.4rem;
    font-weight: bold;
    color: #3b82f6;
}

.stat-label {
    font-size: 0.9rem;
    color: #666;
}
</style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.markdown('<div class="title">📄 RecText 3.0</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Extract text from images using AI-powered OCR (EasyOCR)</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload an image (PNG, JPG, JPEG, WEBP)", type=["png", "jpg", "jpeg", "webp"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="🖼️ Uploaded Image", use_container_width=True)

        with st.spinner("🔍 Extracting text..."):
            reader = easyocr.Reader(['en'], gpu=False)
            image_np = np.array(image)
            results = reader.readtext(image_np)
            extracted_text = '\n'.join([text for _, text, conf in results if conf > 0.5])

        if extracted_text.strip():
            st.success("✅ Text extracted successfully!")
            st.text_area("Extracted Text", extracted_text, height=220)

            col1, col2, col3 = st.columns(3)
            col1.markdown(f'<div class="stat-box"><div class="stat-number">{len(extracted_text.split())}</div><div class="stat-label">Words</div></div>', unsafe_allow_html=True)
            col2.markdown(f'<div class="stat-box"><div class="stat-number">{len(extracted_text)}</div><div class="stat-label">Characters</div></div>', unsafe_allow_html=True)
            col3.markdown(f'<div class="stat-box"><div class="stat-number">{len(extracted_text.splitlines())}</div><div class="stat-label">Lines</div></div>', unsafe_allow_html=True)

            st.download_button("📥 Download Text", data=extracted_text, file_name="extracted_text.txt", mime="text/plain")
        else:
            st.warning("⚠️ No text detected. Try a clearer image.")
    else:
        st.info("📎 Upload an image to get started.")

    st.markdown('</div>', unsafe_allow_html=True)






