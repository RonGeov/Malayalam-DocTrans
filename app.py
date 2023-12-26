from flask import Flask, render_template, request, jsonify
from pdf_ocr import scan_text
from googletrans import Translator
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'file_uploads'

# Set up Google Translator
translator = Translator()
def upload_file(file):
    if file.filename.endswith(".pdf"):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return f"{app.config['UPLOAD_FOLDER']}/{file.filename}"
    else:
        raise ValueError("not a pdf file")

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files['file']
        filename = upload_file(file)
        text = scan_text(filename)
        translated_text = translator.translate(text, src='ml', dest='en').text
        return render_template('result.html',original_text=text, translated_text=translated_text)
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    text = request.form['text']
    translated_text = translator.translate(text, src='ml', dest='en').text
    return jsonify(original_text=text, translated_text=translated_text)

if __name__ == '__main__':
    app.run(debug=True)
