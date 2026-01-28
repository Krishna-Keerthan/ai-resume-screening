# backend/app/models/job.py
from datetime import datetime
from bson import ObjectId

class Job:
    def __init__(self, db):
        self.collection = db['jobs']
    
    def create_job(self, recruiter_id, title, description, required_skills, experience_required):
        """Create job posting"""
        job = {
            'recruiter_id': ObjectId(recruiter_id),
            'title': title,
            'description': description,
            'required_skills': required_skills,
            'experience_required': experience_required,
            'posted_at': datetime.utcnow(),
            'is_active': True
        }
        result = self.collection.insert_one(job)
        return str(result.inserted_id)
    
    def get_all_active_jobs(self):
        """Get all active jobs"""
        return list(self.collection.find({'is_active': True}))
    
    def get_job_by_id(self, job_id):
        """Get job by ID"""
        return self.collection.find_one({'_id': ObjectId(job_id)})