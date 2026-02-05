# backend/test_parser.py
from app.services.resume_parser import parse_resume, extract_basic_info
import os

# Test with sample files
test_files = [
    'uploads/000000000000000000000000/Krishna_Keerthan_Resume_20260128_121331.pdf'
    # 'uploads/sample_resume.pdf',
    # 'uploads/sample_resume.docx'
]

for file_path in test_files:
    if os.path.exists(file_path):
        print(f"\n{'='*50}")
        print(f"Testing: {file_path}")
        print('='*50)
        
        text = parse_resume(file_path)
        if text:
            print(f"\nExtracted Text (first 500 chars):\n{text[:500]}...")
            
            info = extract_basic_info(text)
            print(f"\nBasic Info:")
            print(f"Email: {info['email']}")
            print(f"Phone: {info['phone']}")
            print(f"LinkedIn: {info['linkedin']}")
        else:
            print("Failed to extract text")
    else:
        print(f"File not found: {file_path}")