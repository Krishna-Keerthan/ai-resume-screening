# backend/app/models/user.py
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, db):
        self.collection = db['users']
    
    def create_user(self, email, password, role='candidate'):
        """Create new user"""
        user = {
            'email': email,
            'password_hash': generate_password_hash(password),
            'role': role,  # 'candidate' or 'recruiter'
            'created_at': datetime.utcnow()
        }
        result = self.collection.insert_one(user)
        return str(result.inserted_id)
    
    def find_by_email(self, email):
        """Find user by email"""
        return self.collection.find_one({'email': email})
    
    def verify_password(self, user, password):
        """Check password"""
        return check_password_hash(user['password_hash'], password)