# backend/app/services/resume_parser.py
import os
from app.services.pdf_parser import extract_text_from_pdf
from app.services.docx_parser import extract_text_from_docx

def parse_resume(file_path):
    """Parse resume based on file type"""
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    
    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext == '.docx':
        return extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def extract_basic_info(text):
    """Extract basic information from resume text"""
    import re
    
    info = {
        'email': None,
        'phone': None,
        'linkedin': None
    }
    
    # Extract email
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    if emails:
        info['email'] = emails[0]
    
    # Extract phone
    phone_pattern = r'\b(?:\+?\d{1,3}[\s-]?)?(?:\(\d{3}\)|\d{3})[\s-]?\d{3}[\s-]?\d{4}\b|\b(?:\+?\d{1,3}[\s-]?)?\d{5}[\s-]?\d{5}\b|\b(?:\+?\d{1,3})?\d{10}\b'
    phones = re.findall(phone_pattern, text)
    if phones:
        info['phone'] = phones[0]
    
    # Extract LinkedIn
    linkedin_pattern = r'\b(?:https?:\/\/)?(?:www\.)?linkedin\.com\/(in|pub|company)\/[A-Za-z0-9\-_%]+(?:\/[A-Za-z0-9\-_%]+)?\/?\b'
    linkedins = re.findall(linkedin_pattern, text, re.IGNORECASE)
    if linkedins:
        info['linkedin'] = linkedins[0]
    
    return info