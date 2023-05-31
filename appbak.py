from flask import Flask, render_template, request
import PyPDF2
from googletrans import Translator

app = Flask(__name__)

# Set up Google Translator
translator = Translator(service_urls=['translate.google.com'])

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files['file']
        pdf = PyPDF2.PdfReader(file)
        text = ''
        #for page in range(len(pdf.pages)):
         #   text += pdf.pages[page].extract_text()
        #translated_text = translator.translate(text, src='ml', dest='en').json()
        return render_template('result.html',text=text)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
