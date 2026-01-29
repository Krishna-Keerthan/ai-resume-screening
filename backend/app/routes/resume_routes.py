# backend/app/routes/resume_routes.py
from flask import Blueprint, request, jsonify, current_app
from app.utils.file_handler import save_uploaded_file
from bson import ObjectId
from app.services.resume_parser import parse_resume, extract_basic_info

resume_bp = Blueprint('resume', __name__, url_prefix='/api/resume')

@resume_bp.route('/upload', methods=['POST'])
def upload_resume():
    """Upload and parse resume file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        user_id = request.form.get('user_id', '000000000000000000000000')
        
        # Save file
        file_path = save_uploaded_file(file, user_id)
        if not file_path:
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Parse resume
        parsed_text = parse_resume(file_path)
        if not parsed_text:
            return jsonify({'error': 'Failed to parse resume'}), 500
        
        basic_info = extract_basic_info(parsed_text)
        
        # Save to database
        resume_id = current_app.resume_model.create_resume(
            user_id=user_id,
            filename=file.filename,
            file_path=file_path
        )
        
        # Update with parsed data
        current_app.resume_model.update_parsed_data(resume_id, {
            'parsed_text': parsed_text,
            'email': basic_info['email'],
            'phone': basic_info['phone'],
            'linkedin': basic_info['linkedin']
        })
        
        return jsonify({
            'message': 'Resume uploaded and parsed successfully',
            'resume_id': resume_id,
            'filename': file.filename,
            'text_length': len(parsed_text),
            'basic_info': basic_info
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