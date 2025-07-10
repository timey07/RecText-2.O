import streamlit as st
from PIL import Image
import numpy as np
import easyocr

st.set_page_config(
    page_title="RecText 3.0",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("📄 RecText 3.0")
st.write("Upload an image and extract text using EasyOCR.")

uploaded = st.file_uploader(
    "Choose PNG, JPG, JPEG or WEBP", 
    type=["png", "jpg", "jpeg", "webp"]
)

if uploaded:
    img = Image.open(uploaded)
    st.image(img, use_column_width=True)

    with st.spinner("Extracting text…"):
        reader = easyocr.Reader(["en"], gpu=False)
        arr = np.array(img)
        results = reader.readtext(arr)
        text = "\n".join([t for (_, t, _) in results])

    if text.strip():
        st.text_area("📝 Extracted Text", text, height=200)
        st.download_button("📥 Download .txt", text, file_name="extracted_text.txt")
    else:
        st.warning("No text detected. Try a different image.")








