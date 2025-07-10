from flask import Flask, request, jsonify
from flask_cors import CORS
import easyocr
from PIL import Image
import numpy as np
import io

app = Flask(__name__)
CORS(app)

reader = easyocr.Reader(['en'])

@app.route('/extract', methods=['POST'])
def extract_text():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    image_bytes = image_file.read()
    image = Image.open(io.BytesIO(image_bytes))

    image_np = np.array(image) 
    results = reader.readtext(image_np)

    extracted = '\n'.join([text for _, text, _ in results])
    return jsonify({'text': extracted})

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

