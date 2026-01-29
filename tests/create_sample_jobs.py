# backend/create_sample_jobs.py
from app import create_app
import json
from bson.objectid import ObjectId


app = create_app()

sample_jobs = [
    {
        "recruiter_id": "000000000000000000000001",
        "title": "Senior Python Developer",
        "description": """
We are seeking an experienced Python Developer to join our backend team.

Responsibilities:
- Design and develop RESTful APIs using Flask/Django
- Work with MongoDB and PostgreSQL databases
- Implement microservices architecture
- Write clean, maintainable code
- Collaborate with frontend developers

Requirements:
- 5+ years of Python development experience
- Strong knowledge of Flask or Django framework
- Experience with MongoDB and PostgreSQL
- Proficiency in Docker and Kubernetes
- Understanding of REST API design principles
- Experience with Git version control
- Knowledge of cloud platforms (AWS/Azure)

Nice to have:
- Machine Learning experience
- React.js knowledge
- DevOps experience
        """,
        "required_skills": ["python", "flask", "django", "mongodb", "postgresql", "docker", "kubernetes", "rest api", "git"],
        "experience_required": 5,
        "location": "Remote",
        "salary_range": "$100k-$140k",
        "employment_type": "Full-time",
        "company": "TechCorp Inc."
    },
    {
        "recruiter_id": "000000000000000000000001",
        "title": "Full Stack Developer",
        "description": """
Looking for a Full Stack Developer to build modern web applications.

Responsibilities:
- Develop frontend using React.js
- Build backend APIs with Node.js/Express
- Work with MongoDB database
- Deploy applications on AWS
- Participate in agile development

Requirements:
- 3+ years of full stack development
- Strong JavaScript/TypeScript skills
- Experience with React.js and Node.js
- Knowledge of MongoDB
- Familiarity with AWS services
- Understanding of responsive design

Nice to have:
- Next.js experience
- GraphQL knowledge
- CI/CD pipeline experience
        """,
        "required_skills": ["javascript", "typescript", "react", "nodejs", "express", "mongodb", "aws", "html", "css"],
        "experience_required": 3,
        "location": "Hybrid - New York",
        "salary_range": "$80k-$110k",
        "employment_type": "Full-time",
        "company": "StartupXYZ"
    },
    {
        "recruiter_id": "000000000000000000000001",
        "title": "Data Scientist",
        "description": """
Join our AI team as a Data Scientist to work on machine learning projects.

Responsibilities:
- Build and deploy machine learning models
- Analyze large datasets using Python
- Create data visualizations
- Collaborate with engineering team
- Research new ML techniques

Requirements:
- 2+ years in data science/ML
- Strong Python skills (pandas, NumPy, scikit-learn)
- Experience with TensorFlow or PyTorch
- Knowledge of statistics and probability
- SQL and database skills
- Experience with Jupyter notebooks

Nice to have:
- NLP experience
- Deep learning expertise
- Big data tools (Spark, Hadoop)
        """,
        "required_skills": ["python", "machine learning", "tensorflow", "pytorch", "pandas", "numpy", "scikit-learn", "sql", "statistics"],
        "experience_required": 2,
        "location": "Remote",
        "salary_range": "$90k-$130k",
        "employment_type": "Full-time",
        "company": "AI Solutions Ltd."
    },
    {
        "recruiter_id": "000000000000000000000001",
        "title": "Junior Frontend Developer",
        "description": """
Entry-level position for Frontend Developer to work on web applications.

Responsibilities:
- Build responsive web pages using React
- Work with REST APIs
- Implement UI designs
- Write clean, maintainable code
- Learn from senior developers

Requirements:
- 0-1 years of experience
- Knowledge of HTML, CSS, JavaScript
- Basic understanding of React
- Familiarity with Git
- Good problem-solving skills
- Willingness to learn

Nice to have:
- TypeScript knowledge
- Any backend experience
- Understanding of UI/UX principles
        """,
        "required_skills": ["javascript", "react", "html", "css", "git"],
        "experience_required": 0,
        "location": "On-site - San Francisco",
        "salary_range": "$60k-$80k",
        "employment_type": "Full-time",
        "company": "WebDev Co."
    },
    {
        "recruiter_id": "000000000000000000000001",
        "title": "DevOps Engineer",
        "description": """
Seeking a DevOps Engineer to manage our cloud infrastructure.

Responsibilities:
- Manage AWS/Azure infrastructure
- Build CI/CD pipelines
- Implement monitoring and logging
- Automate deployment processes
- Ensure system reliability and security

Requirements:
- 4+ years of DevOps experience
- Strong knowledge of AWS or Azure
- Experience with Docker and Kubernetes
- Proficiency in scripting (Python, Bash)
- Knowledge of Terraform or Ansible
- Understanding of networking and security

Nice to have:
- Experience with Jenkins or GitLab CI
- Monitoring tools (Prometheus, Grafana)
- Database administration skills
        """,
        "required_skills": ["aws", "azure", "docker", "kubernetes", "terraform", "ansible", "python", "bash", "ci/cd", "jenkins"],
        "experience_required": 4,
        "location": "Remote",
        "salary_range": "$110k-$150k",
        "employment_type": "Full-time",
        "company": "CloudOps Inc."
    }
]

with app.app_context():
    print("Creating sample jobs...")
    for job_data in sample_jobs:
        try:
            job_id = app.job_model.create_job(
                recruiter_id=job_data['recruiter_id'],
                title=job_data['title'],
                description=job_data['description'],
                required_skills=job_data['required_skills'],
                experience_required=job_data['experience_required']
            )
            
            # Update with additional fields
            app.db['jobs'].update_one(
                {'_id': ObjectId(job_id)},
                {'$set': {
                    'location': job_data['location'],
                    'salary_range': job_data['salary_range'],
                    'employment_type': job_data['employment_type'],
                    'company': job_data['company']
                }}
            )
            
            print(f"✓ Created: {job_data['title']} (ID: {job_id})")
        except Exception as e:
            print(f"✗ Error creating {job_data['title']}: {e}")
    
    print("\nDone! Created sample jobs in database.")