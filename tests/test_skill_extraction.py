# backend/test_skill_extraction.py
from app.services.skill_extractor import SkillExtractor

sample_resume = """
John Doe
Software Engineer

EXPERIENCE:
Senior Python Developer at Tech Corp (2020-2023)
- 5 years of experience in backend development
- Developed REST APIs using Flask and FastAPI
- Worked with MongoDB and PostgreSQL databases
- Implemented machine learning models using scikit-learn and TensorFlow
- Collaborated with cross-functional teams using Agile methodologies

SKILLS:
Programming: Python, JavaScript, TypeScript, Java
Web: React.js, Node.js, Express.js, Django, Flask
Databases: MongoDB, PostgreSQL, MySQL, Redis
Cloud: AWS, Docker, Kubernetes
ML/AI: TensorFlow, PyTorch, scikit-learn, pandas, NumPy

EDUCATION:
B.Tech in Computer Science (2016-2020)
"""

sample_job = """
Python Backend Developer

Requirements:
- 3+ years of experience in Python development
- Strong knowledge of Flask or Django
- Experience with MongoDB and PostgreSQL
- Familiarity with Docker and Kubernetes
- REST API development
- Machine Learning experience is a plus
- Good understanding of Agile methodologies

Required Skills:
Python, Flask, MongoDB, PostgreSQL, Docker, REST API, Git
"""

# Test extraction
extractor = SkillExtractor()

print("RESUME ANALYSIS")
print("="*50)
resume_skills = extractor.extract_skills_with_ner(sample_resume)
print(f"Skills found: {len(resume_skills)}")
print(resume_skills)

experience = extractor.extract_experience_years(sample_resume)
print(f"\nYears of experience: {experience}")

print("\n\nJOB ANALYSIS")
print("="*50)
job_skills = extractor.extract_skills_with_ner(sample_job)
print(f"Required skills: {len(job_skills)}")
print(job_skills)

print("\n\nSKILL MATCH ANALYSIS")
print("="*50)
match_result = extractor.calculate_skill_match(resume_skills, job_skills)
print(f"Match Percentage: {match_result['match_percentage']}%")
print(f"\nMatched Skills ({len(match_result['matched_skills'])}):")
print(match_result['matched_skills'])
print(f"\nMissing Skills ({len(match_result['missing_skills'])}):")
print(match_result['missing_skills'])