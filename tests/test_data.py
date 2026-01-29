from app import create_app
from datetime import datetime

app = create_app()

with app.app_context():
    # Create test users
    candidate_id = app.user_model.create_user(
        email='candidate@test.com',
        password='password123',
        role='candidate'
    )
    print(f"Created candidate: {candidate_id}")
    
    recruiter_id = app.user_model.create_user(
        email='recruiter@test.com',
        password='password123',
        role='recruiter'
    )
    print(f"Created recruiter: {recruiter_id}")
    
    # Create test job
    job_id = app.job_model.create_job(
        recruiter_id=recruiter_id,
        title='Python Developer',
        description='We are looking for a Python developer with experience in Flask and React',
        required_skills=['Python', 'Flask', 'React', 'MongoDB', 'REST API'],
        experience_required=2
    )
    print(f"Created job: {job_id}")