# backend/app/__init__.py
from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from config import Config
from app.routes.resume_routes import resume_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    
    # MongoDB connection
    client = MongoClient(app.config['MONGO_URI'])
    app.db = client['resume_screening']
    
    # Initialize models
    from app.models.user import User
    from app.models.resume import Resume
    from app.models.job import Job
    from app.models.match import Match
    
    app.user_model = User(app.db)
    app.resume_model = Resume(app.db)
    app.job_model = Job(app.db)
    app.match_model = Match(app.db)

    
    app.register_blueprint(resume_bp)
    
    return app