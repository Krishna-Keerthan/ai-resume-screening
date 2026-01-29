# backend/test_tfidf.py
from app.services.tfidf_service import TfidfService

sample_resume = """
John Doe
Software Engineer with 5 years of experience

EXPERIENCE:
Senior Python Developer at Tech Corp (2020-2023)
- Developed REST APIs using Flask and FastAPI
- Worked with MongoDB and PostgreSQL databases
- Implemented machine learning models using scikit-learn
- Built microservices architecture with Docker and Kubernetes
- Collaborated with cross-functional teams using Agile methodologies

SKILLS:
Python, JavaScript, React, Node.js, MongoDB, PostgreSQL, 
Flask, FastAPI, Docker, Kubernetes, AWS, Git, 
Machine Learning, scikit-learn, TensorFlow, pandas

EDUCATION:
B.Tech in Computer Science (2016-2020)
"""

sample_job = """
Python Backend Developer

We are looking for an experienced Python developer to join our team.

Responsibilities:
- Design and develop REST APIs
- Work with MongoDB and PostgreSQL
- Implement microservices using Docker
- Collaborate with frontend team
- Follow Agile practices

Requirements:
- 3+ years of Python development experience
- Strong knowledge of Flask or Django
- Experience with MongoDB and PostgreSQL
- Familiarity with Docker and Kubernetes
- Understanding of REST API design
- Experience with Git version control

Nice to have:
- Machine Learning experience
- AWS experience
- React knowledge
"""

# Test TF-IDF
tfidf_service = TfidfService()

print("CALCULATING SIMILARITY")
print("="*50)

similarity = tfidf_service.calculate_similarity(sample_resume, sample_job)
print(f"Cosine Similarity: {similarity:.4f}")

ats_score = tfidf_service.calculate_ats_score(sample_resume, sample_job)
print(f"ATS Score: {ats_score}/100")

print("\n\nTOP RESUME KEYWORDS")
print("="*50)
resume_keywords = tfidf_service.get_top_keywords(sample_resume, top_n=15)
for keyword, score in resume_keywords:
    print(f"{keyword}: {score:.4f}")

print("\n\nTOP JOB KEYWORDS")
print("="*50)
job_keywords = tfidf_service.get_top_keywords(sample_job, top_n=15)
for keyword, score in job_keywords:
    print(f"{keyword}: {score:.4f}")