
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
    layout="centered",
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
        padding: 2rem;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
    }
    
    .main-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 24px;
        padding: 3rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        max-width: 800px;
        margin: 0 auto;
    }
    
    .hero-section {
        text-align: center;
        margin-bottom: 3rem;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.7);
        margin-bottom: 2rem;
    }
    
    .upload-area {
        border: 2px dashed rgba(102, 126, 234, 0.5);
        border-radius: 16px;
        padding: 3rem;
        text-align: center;
        background: rgba(102, 126, 234, 0.1);
        margin-bottom: 2rem;
        transition: all 0.3s ease;
    }
    
    .upload-area:hover {
        border-color: rgba(102, 126, 234, 0.8);
        background: rgba(102, 126, 234, 0.15);
    }
    
    .upload-text {
        color: rgba(255, 255, 255, 0.8);
        font-size: 1.1rem;
        margin-bottom: 1rem;
    }
    
    .upload-subtext {
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.9rem;
    }
    
    .result-section {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 2rem;
        margin-top: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stats-container {
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        margin-top: 1.5rem;
    }
    
    .stat-card {
        background: rgba(102, 126, 234, 0.2);
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        flex: 1;
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
    
    .stDownloadButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.5rem !important;
    }
    
    .stSuccess {
        background: rgba(34, 197, 94, 0.2) !important;
        border: 1px solid rgba(34, 197, 94, 0.3) !important;
        border-radius: 12px !important;
        color: #22c55e !important;
    }
    
    .stWarning {
        background: rgba(251, 191, 36, 0.2) !important;
        border: 1px solid rgba(251, 191, 36, 0.3) !important;
        border-radius: 12px !important;
        color: #fbbf24 !important;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.2) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        border-radius: 12px !important;
        color: #ef4444 !important;
    }
    
    .stSpinner {
        color: #667eea !important;
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

def get_image_download_link(image, filename="processed_image.png"):
    """Generate a download link for the processed image"""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f'<a href="data:image/png;base64,{img_str}" download="{filename}">Download Processed Image</a>'

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
    st.markdown('<div class="upload-area">', unsafe_allow_html=True)
    st.markdown('<div class="upload-text">📤 Upload your image</div>', unsafe_allow_html=True)
    st.markdown('<div class="upload-subtext">Supports PNG, JPG, JPEG, and WEBP formats</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "",
        type=['png', 'jpg', 'jpeg', 'webp'],
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    if uploaded_file is not None:
        try:
            # Load and display the image
            image = Image.open(uploaded_file)
            
            # Display the uploaded image
            st.image(
                image,
                caption="📷 Uploaded Image",
                use_column_width=True
            )
            
            # Extract text button
            if st.button("🔍 Extract Text", key="extract_btn"):
                with st.spinner("🔄 Analyzing image and extracting text..."):
                    extracted_text, ocr_results = extract_text_from_image(image)
                
                # Store results in session state
                st.session_state.extracted_text = extracted_text
                st.session_state.ocr_results = ocr_results
                st.session_state.image_processed = True
            
            # Display results if available
            if hasattr(st.session_state, 'image_processed') and st.session_state.image_processed:
                st.markdown('<div class="result-section">', unsafe_allow_html=True)
                
                if st.session_state.extracted_text.strip():
                    st.success("✅ Text extracted successfully!")
                    
                    # Text area with extracted text
                    st.text_area(
                        "📝 Extracted Text",
                        value=st.session_state.extracted_text,
                        height=300,
                        help="You can edit the extracted text here"
                    )
                    
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
                
                st.markdown('</div>', unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"❌ Error processing image: {str(e)}")
    
    else:
        st.info("👆 Please upload an image to begin text extraction")
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()







