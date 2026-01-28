import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://your-connection-string')
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    UPLOAD_FOLDER = 'uploads'
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
    ALLOWED_EXTENSIONS = {'pdf', 'docx'}