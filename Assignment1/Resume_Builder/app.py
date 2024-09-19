from flask import Flask, render_template, request
import google.generativeai as genai
from dotenv import load_dotenv
import os
import PyPDF2
from docx import Document
from memory_profiler import profile
import threading
import gc
import time
import logging

load_dotenv()

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

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
@profile
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

def log_gc_stats():
    while True:
        gc_stats = gc.get_stats()
        print(f"GC stats: {gc_stats}")
        time.sleep(1)  # Log GC stats every 60 seconds

if __name__ == '__main__':
    start_time = time.time()
    print(f"Application starting...")

    gc_thread = threading.Thread(target=log_gc_stats, daemon=True)
    gc_thread.start()

    app.run()

    end_time = time.time()
    startup_time = end_time - start_time
    print(f"Application startup time: #{startup_time} seconds")
