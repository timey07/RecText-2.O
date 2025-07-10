## 📄 RecText 3.O – OCR Text Extractor

[![Live App](https://img.shields.io/badge/Live%20App-rectext3o.streamlit.app-blue?logo=streamlit\&logoColor=white)](https://rectext3o.streamlit.app/)

**RecText 3.O** is a sleek and responsive web app that extracts text from images using AI-powered OCR (Optical Character Recognition). Built with **Streamlit** and **EasyOCR**, it’s designed to be simple, fast, and accessible.

---

### ⚙️ Tech Stack

* **Frontend/UI**: Streamlit + Custom CSS
* **Backend OCR Engine**: EasyOCR (open-source)
* **Image Processing**: Pillow + NumPy
* **Deployment**: Streamlit Community Cloud

---

### 🖼 Supported Image Formats

* PNG
* JPG / JPEG
* WEBP

📏 **Max file size**: 5MB

---

### 🛠️ How to Run Locally

If you'd like to use the code and run this project on your own machine:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/RecText-3.O.git
   cd RecText-3.O
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app with Streamlit**:

   ```bash
   streamlit run app.py
   ```

4. **Visit in browser**:
   Navigate to `http://localhost:8501` to use the app locally.

---

### 🧠 Features

* Side-by-side layout for image and extracted text
* Clean, modern UI with responsive design
* OCR text extraction powered by open-source EasyOCR
* Download extracted text as a `.txt` file
* Maximum file size enforcement (5MB)

---

### 🙌 Credits

* [EasyOCR](https://github.com/JaidedAI/EasyOCR) – Open-source OCR engine
* [Streamlit](https://streamlit.io) – Rapid frontend for data apps
* Designed and built with love for learning and utility 🤍✨
