# --- RecText 3.O ------------------------------------------------------------
# Simple and clean Streamlit UI for text extraction with EasyOCR
# ---------------------------------------------------------------------------
import streamlit as st
import easyocr
from PIL import Image
import numpy as np

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="RecText 3.O",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="auto",
)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("🚀 How to use")
    st.markdown(
        "1. Upload an image containing text.\n"
        "2. Wait a moment while we detect the text.\n"
        "3. Copy the extracted text or download it as a `.txt` file."
    )
    st.markdown("---")
    st.caption("Powered by EasyOCR")

# ---------------------------------------------------------------------------
# Main UI
# ---------------------------------------------------------------------------
st.title("📄 RecText 3.O")
st.caption("A lightweight tool to extract text from images.")

uploaded_file = st.file_uploader("Upload your image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Display uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Selected Image", use_container_width=True)

    # OCR processing
    with st.spinner("Reading text ..."):
        reader = easyocr.Reader(["en"], gpu=False)
        results = reader.readtext(np.array(image))
        extracted_text = "\n".join([text for _, text, _ in results])

    st.markdown("---")

    if extracted_text.strip():
        st.subheader("Detected Text")
        st.text_area(label="", value=extracted_text, height=220)
        st.download_button(
            label="📥 Download text",
            data=extracted_text,
            file_name="extracted_text.txt",
            mime="text/plain",
        )
    else:
        st.warning("No text detected. Try another image.")
else:
    st.info("Upload an image to get started ☝️")




