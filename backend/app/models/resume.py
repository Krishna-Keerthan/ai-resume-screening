# backend/app/models/resume.py
from datetime import datetime
from bson import ObjectId

class Resume:
    def __init__(self, db):
        self.collection = db['resumes']
    
    def create_resume(self, user_id, filename, file_path):
        """Store resume metadata"""
        resume = {
            'user_id': ObjectId(user_id),
            'filename': filename,
            'file_path': file_path,
            'parsed_text': None,
            'skills': [],
            'experience_years': 0,
            'education': [],
            'uploaded_at': datetime.utcnow()
        }
        result = self.collection.insert_one(resume)
        return str(result.inserted_id)
    
    def update_parsed_data(self, resume_id, parsed_data):
        """Update resume with parsed information"""
        self.collection.update_one(
            {'_id': ObjectId(resume_id)},
            {'$set': parsed_data}
        )
    
    def get_resume_by_id(self, resume_id):
        """Get resume by ID"""
        return self.collection.find_one({'_id': ObjectId(resume_id)})
    
    def get_user_resumes(self, user_id):
        """Get all resumes for a user"""
        return list(self.collection.find({'user_id': ObjectId(user_id)}))