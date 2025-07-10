# --- RecText 3.O ------------------------------------------------------------
# Simple and clean Streamlit UI for text extraction with EasyOCR
# ---------------------------------------------------------------------------
import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import io

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
=======
# Page configuration
st.set_page_config(
    page_title="RecText 3.0",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for clean, modern design
st.markdown("""
<style>
    /* Hide Streamlit elements for cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main styling */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Container styling */
    .main-container {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        margin: 2rem auto;
        max-width: 800px;
    }
    
    /* Title styling */
    .app-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .app-subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Upload area styling */
    .upload-section {
        border: 2px dashed #d1d5db;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        margin: 2rem 0;
        background: #f9fafb;
        transition: all 0.3s ease;
    }
    
    .upload-section:hover {
        border-color: #667eea;
        background: #f0f4f8;
    }
    
    /* Results styling */
    .result-container {
        background: #f8fafc;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    /* Button styling */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
    }
    
    /* Text area styling */
    .stTextArea textarea {
        border-radius: 8px;
        border: 2px solid #e5e7eb;
        font-family: 'Monaco', 'Menlo', monospace;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Main app content
def main():
    # Header
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.markdown('<h1 class="app-title">📄 RecText 3.0</h1>', unsafe_allow_html=True)
    st.markdown('<p class="app-subtitle">Advanced OCR Text Extraction • Upload • Extract • Download</p>', unsafe_allow_html=True)
    
    # File uploader
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "",
        type=["png", "jpg", "jpeg", "webp"],
        help="Supported formats: PNG, JPG, JPEG, WEBP"
    )
    
    if not uploaded_file:
        st.markdown("""
        <div style="text-align: center; color: #6b7280;">
            <h3 style="margin: 0; color: #374151;">📸 Drop your image here</h3>
            <p style="margin: 0.5rem 0 0 0;">or click to browse your files</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Process uploaded file
    if uploaded_file:
        try:
            # Load and display image
            image = Image.open(uploaded_file)
            
            # Image preview
            st.markdown("### 🖼️ Image Preview")
            st.image(image, use_column_width=True, caption=f"Uploaded: {uploaded_file.name}")
            
            # Extract text
            with st.spinner("🔍 Analyzing image and extracting text..."):
                # Convert image to numpy array
                image_np = np.array(image)
                
                # Initialize EasyOCR reader
                reader = easyocr.Reader(['en'], gpu=False)
                
                # Extract text
                results = reader.readtext(image_np)
                extracted_text = '\n'.join([text for _, text, confidence in results if confidence > 0.5])
            
            # Display results
            st.markdown("### 📝 Extracted Text")
            
            if extracted_text.strip():
                st.markdown('<div class="result-container">', unsafe_allow_html=True)
                st.success("✅ Text extraction completed successfully!")
                
                # Text output
                st.text_area(
                    "Text Output:",
                    value=extracted_text,
                    height=200,
                    help="You can copy this text or download it as a file"
                )
                
                # Download button
                st.download_button(
                    label="📥 Download as Text File",
                    data=extracted_text,
                    file_name=f"extracted_text_{uploaded_file.name.split('.')[0]}.txt",
                    mime="text/plain"
                )
                
                # Statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Words", len(extracted_text.split()))
                with col2:
                    st.metric("Characters", len(extracted_text))
                with col3:
                    st.metric("Lines", len(extracted_text.split('\n')))
                
                st.markdown('</div>', unsafe_allow_html=True)
                
            else:
                st.error("❌ No text detected in the image. Please try:")
                st.markdown("""
                - A clearer, higher resolution image
                - Better lighting conditions
                - Images with more contrast
                - Ensuring text is not too small or blurry
                """)
        
        except Exception as e:
            st.error(f"❌ Error processing image: {str(e)}")
            st.info("Please try uploading a different image or check the file format.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: #6b7280; font-size: 0.9rem;">Built with Streamlit & EasyOCR</p>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()





