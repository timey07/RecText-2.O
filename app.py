import streamlit as st
import easyocr
from PIL import Image
import numpy as np

st.set_page_config(page_title="RecText 3.O", layout="wide")
st.title("📄 RecText 3.O - Image to Text Extractor")
st.markdown("Upload an image and extract readable text using AI.")

uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    image_np = np.array(image)

    col1, col2 = st.columns([1, 1])  

    with col1:
        st.markdown("### 📷 Uploaded Image")
        st.image(image, caption="Uploaded Image", use_container_width=True)

    with col2:
        st.markdown("### 🔍 Extracted Text")
        with st.spinner("Processing..."):
            reader = easyocr.Reader(['en'])
            results = reader.readtext(image_np)
            extracted_text = '\n'.join([text for _, text, _ in results])

        if extracted_text.strip():
            st.success("✅ Text successfully extracted!")
            st.text_area("📝 Extracted Text", extracted_text, height=300)
            st.download_button(
                "📥 Download as .txt",
                extracted_text,
                file_name="extracted_text.txt",
                mime="text/plain"
            )
        else:
            st.error("❌ No text detected. Please upload a clearer image.")

