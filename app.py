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
    padding: 0;
    margin: 0;
}

#MainMenu, header, footer {
    visibility: hidden;
}

.container {
    background: #ffffffcc;
    border-radius: 20px;
    padding: 2rem;
    max-width: 850px;
    margin: 3rem auto;
    box-shadow: 0 12px 30px rgba(0,0,0,0.08);
}

.title {
    text-align: center;
    font-size: 2.4rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.subtitle {
    text-align: center;
    font-size: 1rem;
    color: #555;
    margin-bottom: 2rem;
}

.upload-area {
    border: 2px dashed #cbd5e1;
    background: #f9fafb;
    padding: 2rem;
    border-radius: 12px;
    text-align: center;
    margin-bottom: 1.5rem;
}

.result-box {
    background: #f8fafc;
    border-radius: 10px;
    padding: 1rem;
    border-left: 4px solid #2563eb;
    margin-top: 1rem;
}

.stDownloadButton > button {
    background: #10b981;
    color: white;
    padding: 0.6rem 1.2rem;
    border: none;
    border-radius: 6px;
    font-weight: 600;
    margin-top: 0.5rem;
    width: 100%;
}

.stDownloadButton > button:hover {
    background: #059669;
}

.stTextArea textarea {
    font-family: 'Courier New', monospace;
    border-radius: 6px;
    border: 1px solid #ddd;
}
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<div class="container">', unsafe_allow_html=True)
    
    st.markdown('<div class="title">📄 RecText 3.0</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Extract text from images using AI-powered OCR (EasyOCR)</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="upload-area">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload an image (PNG, JPG, JPEG, WEBP)", type=["png", "jpg", "jpeg", "webp"])
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="📷 Uploaded Image", use_container_width=True)

            with st.spinner("🔍 Extracting text..."):
                image_np = np.array(image)
                reader = easyocr.Reader(['en'], gpu=False)
                results = reader.readtext(image_np)
                extracted_text = '\n'.join([text for _, text, conf in results if conf > 0.5])

            if extracted_text.strip():
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.success("✅ Text extracted successfully!")
                st.text_area("Text Output", extracted_text, height=220)
                st.download_button("📥 Download as Text File", extracted_text, file_name="extracted_text.txt", mime="text/plain")
                st.markdown('</div>', unsafe_allow_html=True)

                # Stats
                col1, col2, col3 = st.columns(3)
                col1.metric("Words", len(extracted_text.split()))
                col2.metric("Characters", len(extracted_text))
                col3.metric("Lines", len(extracted_text.split('\n')))
            else:
                st.warning("⚠️ No clear text detected. Try a better-quality image.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

    else:
        st.info("📎 Upload an image to begin.")

    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()





