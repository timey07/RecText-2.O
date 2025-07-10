
import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import io
import base64

# Configure the Streamlit page
st.set_page_config(
    page_title="OCR Text Extractor",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main > div {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
        min-height: 100vh;
        padding: 1rem;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
    }
    
    .main-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 24px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .hero-section {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .hero-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.7);
        margin-bottom: 1.5rem;
    }
    
    .upload-section {
        background: rgba(102, 126, 234, 0.1);
        border: 2px dashed rgba(102, 126, 234, 0.5);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .content-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2rem;
        margin-top: 2rem;
    }
    
    .image-section, .text-section {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        height: 500px;
        overflow: hidden;
    }
    
    .section-title {
        color: #667eea;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .stats-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-top: 1.5rem;
    }
    
    .stat-card {
        background: rgba(102, 126, 234, 0.2);
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        border: 1px solid rgba(102, 126, 234, 0.3);
    }
    
    .stat-number {
        font-size: 1.5rem;
        font-weight: 600;
        color: #667eea;
        display: block;
    }
    
    .stat-label {
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.9rem;
        margin-top: 0.25rem;
    }
    
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: white !important;
        font-family: 'Courier New', monospace !important;
        height: 350px !important;
    }
    
    .stDownloadButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        color: white !important;
        font-weight: 600 !important;
        width: 100% !important;
        margin-top: 1rem !important;
    }
    
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 0.75rem 2rem !important;
        width: 100% !important;
    }
    
    .stImage > div {
        border-radius: 12px !important;
        overflow: hidden !important;
    }
    
    @media (max-width: 768px) {
        .content-grid {
            grid-template-columns: 1fr;
        }
        
        .hero-title {
            font-size: 2rem;
        }
        
        .stats-container {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_ocr_reader():
    """Load and cache the EasyOCR reader"""
    return easyocr.Reader(['en'], gpu=False)

def extract_text_from_image(image):
    """Extract text from image using EasyOCR"""
    try:
        # Load the OCR reader
        reader = load_ocr_reader()
        
        # Convert PIL image to numpy array
        image_np = np.array(image)
        
        # Extract text
        results = reader.readtext(image_np)
        
        # Filter results by confidence and extract text
        extracted_texts = []
        for (bbox, text, confidence) in results:
            if confidence > 0.5:  # Only include text with >50% confidence
                extracted_texts.append(text)
        
        return '\n'.join(extracted_texts), results
    except Exception as e:
        st.error(f"Error during text extraction: {str(e)}")
        return "", []

def main():
    # Main container
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Hero section
    st.markdown('''
    <div class="hero-section">
        <h1 class="hero-title">📄 OCR Text Extractor</h1>
        <p class="hero-subtitle">Extract text from images using AI-powered OCR technology</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # File upload section
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.markdown("📤 **Upload your image**")
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['png', 'jpg', 'jpeg', 'webp']
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    if uploaded_file is not None:
        try:
            # Load the image
            image = Image.open(uploaded_file)
            
            # Extract text button
            if st.button("🔍 Extract Text", key="extract_btn"):
                with st.spinner("🔄 Analyzing image and extracting text..."):
                    extracted_text, ocr_results = extract_text_from_image(image)
                
                # Store results in session state
                st.session_state.extracted_text = extracted_text
                st.session_state.ocr_results = ocr_results
                st.session_state.image_processed = True
                st.session_state.uploaded_image = image
            
            # Display results in side-by-side layout if available
            if hasattr(st.session_state, 'image_processed') and st.session_state.image_processed:
                if st.session_state.extracted_text.strip():
                    st.success("✅ Text extracted successfully!")
                    
                    # Side-by-side content
                    st.markdown('<div class="content-grid">', unsafe_allow_html=True)
                    
                    # Left column - Image
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown('<div class="image-section">', unsafe_allow_html=True)
                        st.markdown('<div class="section-title">📷 Uploaded Image</div>', unsafe_allow_html=True)
                        st.image(
                            st.session_state.uploaded_image,
                            use_column_width=True
                        )
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Right column - Text
                    with col2:
                        st.markdown('<div class="text-section">', unsafe_allow_html=True)
                        st.markdown('<div class="section-title">📝 Extracted Text</div>', unsafe_allow_html=True)
                        st.text_area(
                            "",
                            value=st.session_state.extracted_text,
                            height=350,
                            label_visibility="collapsed"
                        )
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Download button
                    st.download_button(
                        label="📥 Download as Text File",
                        data=st.session_state.extracted_text,
                        file_name="extracted_text.txt",
                        mime="text/plain"
                    )
                    
                    # Statistics
                    text = st.session_state.extracted_text
                    word_count = len(text.split())
                    char_count = len(text)
                    line_count = len(text.split('\n'))
                    detection_count = len(st.session_state.ocr_results)
                    
                    st.markdown('''
                    <div class="stats-container">
                        <div class="stat-card">
                            <span class="stat-number">{}</span>
                            <div class="stat-label">Words</div>
                        </div>
                        <div class="stat-card">
                            <span class="stat-number">{}</span>
                            <div class="stat-label">Characters</div>
                        </div>
                        <div class="stat-card">
                            <span class="stat-number">{}</span>
                            <div class="stat-label">Lines</div>
                        </div>
                        <div class="stat-card">
                            <span class="stat-number">{}</span>
                            <div class="stat-label">Detections</div>
                        </div>
                    </div>
                    '''.format(word_count, char_count, line_count, detection_count), 
                    unsafe_allow_html=True)
                    
                else:
                    st.warning("⚠️ No text detected in the image. Please try with a clearer image containing text.")
            
            else:
                # Show image preview before processing
                st.markdown('<div class="content-grid">', unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown('<div class="image-section">', unsafe_allow_html=True)
                    st.markdown('<div class="section-title">📷 Image Preview</div>', unsafe_allow_html=True)
                    st.image(image, use_column_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown('<div class="text-section">', unsafe_allow_html=True)
                    st.markdown('<div class="section-title">📝 Extracted Text</div>', unsafe_allow_html=True)
                    st.info("Click 'Extract Text' to analyze the image")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"❌ Error processing image: {str(e)}")
    
    else:
        st.info("👆 Please upload an image to begin text extraction")
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()








