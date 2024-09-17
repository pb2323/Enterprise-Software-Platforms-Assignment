from flask import Flask, render_template, request
import google.generativeai as genai
from dotenv import load_dotenv
import os
import PyPDF2
from docx import Document

load_dotenv()

app = Flask(__name__)

# Configure the Gemini AI API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.0-pro-latest")

def extract_text_from_pdf(file):
    text = ''
    pdf_reader = PyPDF2.PdfReader(file)
    for page in pdf_reader.pages:
        text += page.extract_text() + '\n'
    return text

def extract_text_from_doc(file):
    doc = Document(file)
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text

def extract_resume_text(file):
    filename = file.filename.lower()
    if filename.endswith('.pdf'):
        return extract_text_from_pdf(file)
    elif filename.endswith('.doc') or filename.endswith('.docx'):
        return extract_text_from_doc(file)
    elif filename.endswith('.txt'):
        return file.read().decode('utf-8')
    else:
        raise ValueError('Unsupported file format')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle file upload
        uploaded_file = request.files['resume']
        if uploaded_file.filename != '':
            try:
                # Extract text from the uploaded file
                resume_text = extract_resume_text(uploaded_file)
                
                # Analyze resume with Gemini AI
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
                print(analysis)

                # Extract sections from the analysis
                try:
                    improvements_section = analysis.split("Improvements:", 1)[1].split("Score:", 1)[0].strip()
                    improvement_items = improvements_section.split('\n')
                    improvements = '<ul>' + ''.join(f'<li>{item.strip("- ").strip()}</li>' for item in improvement_items if item.strip()) + '</ul>'
                except IndexError:
                    improvements = "<p>Error: Unable to extract improvements. The AI response format was unexpected.</p>"
                try:
                    score_section = analysis.split("Score:", 1)[1].strip()
                    score = score_section.split("/10", 1)[0].strip()
                except IndexError:
                    score = "Error: Unable to extract score."
                try:
                    explanation = score_section.split("Explanation:", 1)[1].strip()
                except IndexError:
                    explanation = "Error: Unable to extract explanation."


                return render_template('result.html', 
                                       improvements=improvements, 
                                       score=score, 
                                       explanation=explanation)
            except ValueError as e:
                return render_template('index.html', error=str(e))

    return render_template('index.html')

if __name__ == '__main__':
    app.run()