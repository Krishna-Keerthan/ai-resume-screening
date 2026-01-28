# backend/app/models/match.py
from datetime import datetime
from bson import ObjectId

class Match:
    def __init__(self, db):
        self.collection = db['matches']
    
    def save_match(self, resume_id, job_id, ats_score, skill_match_percentage, missing_skills):
        """Save resume-job match result"""
        match = {
            'resume_id': ObjectId(resume_id),
            'job_id': ObjectId(job_id),
            'ats_score': ats_score,
            'skill_match_percentage': skill_match_percentage,
            'missing_skills': missing_skills,
            'matched_at': datetime.utcnow()
        }
        # Update if exists, insert if not
        self.collection.update_one(
            {'resume_id': ObjectId(resume_id), 'job_id': ObjectId(job_id)},
            {'$set': match},
            upsert=True
        )
    
    def get_matches_for_resume(self, resume_id, limit=10):
        """Get top matches for a resume"""
        return list(
            self.collection.find({'resume_id': ObjectId(resume_id)})
            .sort('ats_score', -1)
            .limit(limit)
        )
    
    def get_matches_for_job(self, job_id):
        """Get all candidates for a job"""
        return list(
            self.collection.find({'job_id': ObjectId(job_id)})
            .sort('ats_score', -1)
        )