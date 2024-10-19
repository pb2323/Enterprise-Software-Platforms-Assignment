# frontend_service.py
from flask import Flask, render_template, request, redirect, url_for
import requests
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

PDF_SERVICE_URL = os.getenv("PDF_SERVICE_URL", "http://127.0.0.1:1234/analyze")
DOC_SERVICE_URL = os.getenv("DOC_SERVICE_URL", "http://127.0.0.1:1235/analyze")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error='No file part')
        
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error='No selected file')
        print(file.filename)
        if file:
            filename = file.filename.lower()
            if filename.endswith('.pdf'):
                service_url = PDF_SERVICE_URL
            elif filename.endswith('.doc') or filename.endswith('.docx'):
                service_url = DOC_SERVICE_URL
            else:
                return render_template('index.html', error='Unsupported file type')
            
            try:
                file_stream = file.stream.read()
                files = {'file': (file.filename, file_stream, file.content_type)}
                response = requests.post(service_url, files=files)
                print(response.json())
                if response.status_code == 200:
                    analysis = response.json()
                    return render_template('result.html', analysis=analysis)
                else:
                    return render_template('index.html', error='Error analyzing file')
            except requests.RequestException:
                return render_template('index.html', error='Error connecting to analysis service')
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)