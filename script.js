const fileInput = document.getElementById('fileInput');
const startBtn = document.getElementById('startBtn');
const preview = document.getElementById('preview');
const progress = document.getElementById('progress');
const textOutput = document.getElementById('textOutput');
const outputContainer = document.getElementById('outputContainer');
const downloadSection = document.getElementById('downloadSection');

let extractedText = '';

// Show image preview
fileInput.onchange = () => {
  const file = fileInput.files[0];
  if (file) {
    preview.src = URL.createObjectURL(file);
    outputContainer.style.display = 'flex';
  }
};

// Call EasyOCR backend
startBtn.onclick = () => {
  const file = fileInput.files[0];
  if (!file) return alert('Please select an image.');

  const formData = new FormData();
  formData.append('image', file);

  progress.textContent = 'Processing...';

fetch('http://13.71.117.59:5000/extract', {
  method: 'POST',
  body: formData
})

    .then(res => res.json())
    .then(data => {
      if (data.text && data.text.trim().length > 0) {
        extractedText = data.text;
        textOutput.value = data.text;
        progress.textContent = 'Done';
        downloadSection.style.display = 'block';
      } else {
        textOutput.value = '❌ No text detected or image very unclear.';
        progress.textContent = 'Failed';
        downloadSection.style.display = 'none';
      }
    })
    .catch(err => {
      progress.textContent = 'Error: ' + err.message;
    });
};

// Download result
function downloadText() {
  const blob = new Blob([extractedText], { type: 'text/plain' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'extracted_text.txt';
  link.click();
}
