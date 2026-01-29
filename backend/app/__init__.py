from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from config import Config
from app.routes.resume_routes import resume_bp
from flask_jwt_extended import JWTManager
from app.utils.error_handler import register_error_handlers


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    # Initialize JWT
    jwt = JWTManager(app)
    
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

    # Register error handlers
    register_error_handlers(app)

    app.register_blueprint(resume_bp)

    from app.routes.analysis_routes import analysis_bp
    app.register_blueprint(analysis_bp)

    
    # backend/app/__init__.py
    from app.routes.job_routes import job_bp
    app.register_blueprint(job_bp)

    # Authentication
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    #Improvements
    from app.routes.improvement_routes import improvement_bp
    app.register_blueprint(improvement_bp)

    # PDF Generation BP
    from app.routes.pdf_routes import pdf_bp
    app.register_blueprint(pdf_bp)
    
    return app