from flask import Flask, render_template, request
import pytesseract
from PIL import Image
import io

from pdf2image import convert_from_path

app = Flask(__name__)


@app.route('/translate', methods=['POST'])
def translate():
    file = request.files['file']
    if file and file.filename.endswith('.pdf'):
        images = convert_from_path(file)
        text = ''
        for image in images:
            text += pytesseract.image_to_string(image, lang='mal')
        return text
    return ''




@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    file = request.files['file']
    if file:
        image = Image.open(io.BytesIO(file.read()))
        text = pytesseract.image_to_string(image, lang='mal')
        return text
    return ''

if __name__ == '__main__':
    app.run(debug=True)
