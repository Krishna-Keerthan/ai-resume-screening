# backend/test_preprocessing.py
from app.services.text_preprocessor import TextPreprocessor

# Sample resume text
sample_text = """
John Doe
Software Engineer
Email: john.doe@email.com
Phone: +1-234-567-8900

EXPERIENCE:
Senior Python Developer at Tech Corp (2020-2023)
- Developed REST APIs using Flask and FastAPI
- Worked with MongoDB and PostgreSQL databases
- Implemented machine learning models using scikit-learn
- Collaborated with cross-functional teams

SKILLS:
Python, JavaScript, React.js, Node.js, MongoDB, SQL, Git, Docker, AWS
Machine Learning, Data Analysis, REST APIs, Microservices

EDUCATION:
B.Tech in Computer Science (2016-2020)
"""

preprocessor = TextPreprocessor()

print("Original Text:")
print(sample_text)
print("\n" + "="*50 + "\n")

print("Preprocessed Text:")
preprocessed = preprocessor.preprocess(sample_text)
print(preprocessed)
print("\n" + "="*50 + "\n")

print("Tokens:")
tokens = preprocessor.get_tokens(sample_text)
print(tokens[:20])  # First 20 tokens
print(f"\nTotal tokens: {len(tokens)}")