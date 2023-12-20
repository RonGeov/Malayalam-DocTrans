import os
import pytesseract
from flask import Flask, render_template, request
from googletrans import Translator
from werkzeug.utils import secure_filename
from pdf2image import convert_from_path

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

translator = Translator()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def translate_malayalam_to_english(file_path):
    images = convert_from_path(file_path)
    text = ''
    for image in images:
        extracted_text = pytesseract.image_to_string(image, lang='mal')
        text += extracted_text + ' '
    translated_text = translator.translate(text, src='ml', dest='en').text
    return translated_text, text


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file uploaded'
        file = request.files['file']
        if file.filename == '':
            return 'No file selected'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            translated_text, original_text = translate_malayalam_to_english(file_path)
            return render_template('result.html', original_text=original_text, translated_text=translated_text)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)