import pytest
from app import extract_text_from_pdf, extract_text_from_doc
from io import BytesIO
from docx import Document
from reportlab.pdfgen import canvas

def test_extract_text_from_pdf():
    # Create a simple PDF in memory using reportlab
    pdf_content = BytesIO()
    c = canvas.Canvas(pdf_content)
    c.drawString(100, 750, "Hello, World!")
    c.save()
    pdf_content.seek(0)
    
    text = extract_text_from_pdf(pdf_content)
    print(f"Extracted text: {text}")
    assert "Hello, World!" in text

def test_extract_text_from_doc():
    # Create a simple DOCX in memory
    doc_content = BytesIO()
    doc = Document()
    doc.add_paragraph("Hello, World!")
    doc.save(doc_content)
    doc_content.seek(0)
    text = extract_text_from_doc(doc_content)
    # print("hereeeee")
    assert "Hello, World!" in text