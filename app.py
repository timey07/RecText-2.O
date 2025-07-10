import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import streamlit.components.v1 as components
import base64
import io

st.set_page_config(
    page_title="RecText-3.O",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%) !important;
        color: white;
    }

    .main-container {
        padding: 2rem;
        max-width: 1200px;
        margin: auto;
    }

    .title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.7);
        margin-bottom: 2rem;
    }

    .content-area {
        display: flex;
        gap: 2rem;
        justify-content: center;
        flex-wrap: wrap;
    }

    .image-box, .text-box {
        flex: 1;
        min-width: 350px;
        max-width: 500px;
    }

    .image-box img {
        border-radius: 12px;
        width: 100%;
        height: auto;
    }

    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: white !important;
        font-family: 'Courier New', monospace !important;
        height: 400px !important;
    }

    .stDownloadButton button, .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.5rem !important;
        width: 100%;
        margin-top: 1rem;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<div class="title">RecText-3.O</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Extract text from images using AI-powered OCR (Upload or Paste)</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Note: Max file size 5MB", type=["png", "jpg", "jpeg", "webp"])

# --- JS to support clipboard paste ---
components.html("""
<script>
document.addEventListener("paste", async (event) => {
    const items = (event.clipboardData || window.clipboardData).items;
    for (const item of items) {
        if (item.type.indexOf("image") !== -1) {
            const file = item.getAsFile();
            const reader = new FileReader();
            reader.onload = function(event) {
                const base64Image = event.target.result;
                const img = new Image();
                img.src = base64Image;
                img.onload = function() {
                    const canvas = document.createElement("canvas");
                    canvas.width = img.width;
                    canvas.height = img.height;
                    const ctx = canvas.getContext("2d");
                    ctx.drawImage(img, 0, 0);
                    const newBase64 = canvas.toDataURL("image/png");
                    const data = newBase64.split(",")[1];
                    fetch("/paste_image", {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify({ data: data })
                    }).then(() => {
                        window.location.reload();
                    });
                };
            };
            reader.readAsDataURL(file);
        }
    }
});
</script>
""", height=0)

if not hasattr(st.session_state, 'image_data'):
    st.session_state.image_data = None

# Receive pasted image if available
if "paste_image" in st.experimental_get_query_params():
    pasted_data = st.experimental_get_query_params()["paste_image"][0]
    try:
        image_bytes = base64.b64decode(pasted_data)
        st.session_state.image_data = Image.open(io.BytesIO(image_bytes))
    except:
        st.warning("Failed to decode pasted image")

if uploaded_file:
    if uploaded_file.size > 5 * 1024 * 1024:
        st.error("File too large. Please upload an image under 5MB.")
    else:
        image = Image.open(uploaded_file)
        st.session_state.image_data = image

if st.session_state.image_data:
    image = st.session_state.image_data

    st.markdown('<div class="content-area">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="image-box">', unsafe_allow_html=True)
        st.image(image)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        if st.button("🔍 Extract Text"):
            with st.spinner("Analyzing image..."):
                reader = easyocr.Reader(["en"], gpu=False)
                results = reader.readtext(np.array(image))
                extracted_text = "\n".join([t for (_, t, conf) in results if conf > 0.5])
                st.session_state.text = extracted_text
                st.session_state.results = results

        if 'text' in st.session_state:
            st.markdown('<div class="text-box">', unsafe_allow_html=True)
            st.text_area("Extracted Text", st.session_state.text, height=400)
            st.download_button("Download as Text File", st.session_state.text, file_name="extracted_text.txt")
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("Upload or paste an image to get started.")

st.markdown('</div>', unsafe_allow_html=True)

