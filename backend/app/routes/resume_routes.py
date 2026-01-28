# backend/app/routes/resume_routes.py
from flask import Blueprint, request, jsonify, current_app
from app.utils.file_handler import save_uploaded_file
from bson import ObjectId

resume_bp = Blueprint('resume', __name__, url_prefix='/api/resume')

@resume_bp.route('/upload', methods=['POST'])
def upload_resume():
    """Upload resume file"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Get user_id from request (for now, use dummy ID)
        # Later we'll get this from JWT token
        user_id = request.form.get('user_id', '000000000000000000000000')
        
        # Save file
        file_path = save_uploaded_file(file, user_id)
        if not file_path:
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Save to database
        resume_id = current_app.resume_model.create_resume(
            user_id=user_id,
            filename=file.filename,
            file_path=file_path
        )
        
        return jsonify({
            'message': 'Resume uploaded successfully',
            'resume_id': resume_id,
            'filename': file.filename
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@resume_bp.route('/<resume_id>', methods=['GET'])
def get_resume(resume_id):
    """Get resume details"""
    try:
        resume = current_app.resume_model.get_resume_by_id(resume_id)
        if not resume:
            return jsonify({'error': 'Resume not found'}), 404
        
        # Convert ObjectId to string for JSON serialization
        resume['_id'] = str(resume['_id'])
        resume['user_id'] = str(resume['user_id'])
        
        return jsonify(resume), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500