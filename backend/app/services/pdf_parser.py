# backend/app/services/pdf_parser.py
import pdfplumber
import re

def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    try:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        # Clean the text
        text = clean_text(text)
        return text
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return None

def clean_text(text):
    """Clean extracted text"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?@#-]', '', text)
    return text.strip()