import streamlit as st
import easyocr
from PIL import Image
import numpy as np

st.set_page_config(page_title="RecText 3.O", layout="centered")

st.title("RecText 3.O")
st.caption("Extract text from images using EasyOCR. Upload an image to get started.")

uploaded_file = st.file_uploader("Upload an image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    with st.spinner("Extracting text..."):
        image_np = np.array(image)
        reader = easyocr.Reader(['en'], gpu=False)
        results = reader.readtext(image_np)
        extracted_text = '\n'.join([text for _, text, _ in results])

    if extracted_text.strip():
        st.success("Text extracted successfully!")
        st.text_area("Extracted Text", extracted_text, height=200)
        st.download_button("Download Text", extracted_text, file_name="extracted_text.txt")
    else:
        st.warning("No text detected. Try another image.")
else:
    st.info("Please upload an image to begin.")




