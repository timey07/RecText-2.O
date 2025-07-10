import streamlit as st
import easyocr
from PIL import Image
import numpy as np

st.set_page_config(page_title="RecText 2.O", layout="centered")
st.title("🧠 RecText 3.O")
st.markdown("### Upload an image to extract text using AI (EasyOCR)")

uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="📷 Uploaded Image", use_column_width=True)

    with st.spinner("🔍 Extracting text..."):
        reader = easyocr.Reader(['en'])
        image_np = np.array(image)
        results = reader.readtext(image_np)
        extracted_text = '\n'.join([text for _, text, _ in results])

    st.divider()

    if extracted_text.strip():
        st.success("✅ Text successfully extracted!")
        st.text_area("📝 Extracted Text", extracted_text, height=250)
        st.download_button(
            "📥 Download as Text File",
            extracted_text,
            file_name="extracted_text.txt",
            mime="text/plain"
        )
    else:
        st.error("❌ No readable text detected. Try a clearer image.")
