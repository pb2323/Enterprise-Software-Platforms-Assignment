# pdf_service.py
from flask import Flask, request, jsonify
import PyPDF2
import google.generativeai as genai
import os
from dotenv import load_dotenv
import io

load_dotenv()

app = Flask(__name__)

# Configure the Gemini AI API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.0-pro-latest")

@app.route('/analyze', methods=['POST'])
def analyze_pdf():
    print (request.files)
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    print (file.filename)
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.lower().endswith('.pdf'):
        try:
            file_stream = io.BytesIO(file.read())
            text = extract_text_from_pdf(file_stream)
            analysis = analyze_resume(text)
            return jsonify(analysis)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Invalid file format'}), 400

def extract_text_from_pdf(file_stream):
    text = ''
    pdf_reader = PyPDF2.PdfReader(file_stream)
    for page in pdf_reader.pages:
        text += page.extract_text() + '\n'
    return text

def analyze_resume(resume_text):
    prompt = f"""Analyze the following resume and provide:
    1. A list of 3-5 specific improvements
    2. A score out of 10, with a brief explanation
    3. Output should not have bold text

    Resume:
    {resume_text}

    Format your response as follows:
    Improvements:
    - [Improvement 1]
    - [Improvement 2]
    - [Improvement 3]

    Score: [X]/10
    Explanation: [Brief explanation for the score]
    """

    response = model.generate_content(prompt)
    analysis = response.text

    # Extract sections from the analysis
    improvements_section = analysis.split("Improvements:", 1)[1].split("Score:", 1)[0].strip()
    improvement_items = improvements_section.split('\n')
    improvements = [item.strip("- ").strip() for item in improvement_items if item.strip()]
    
    score_section = analysis.split("Score:", 1)[1].strip()
    score = score_section.split("/10", 1)[0].strip()
    
    explanation = score_section.split("Explanation:", 1)[1].strip()

    return {
        'improvements': improvements,
        'score': score,
        'explanation': explanation
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234, debug=True)