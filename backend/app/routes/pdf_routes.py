# backend/app/routes/pdf_routes.py
from flask import Blueprint, request, jsonify, send_file, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.decorators import candidate_required
from app.services.pdf_generator import ResumePDFGenerator
from bson import ObjectId
import os
from datetime import datetime

pdf_bp = Blueprint('pdf', __name__, url_prefix='/api/pdf')

@pdf_bp.route('/generate/<resume_id>', methods=['POST'])
@candidate_required
def generate_resume_pdf(resume_id):
    """
    Generate PDF from resume data
    
    Request body:
    {
        "template": "professional",  // or "modern", "creative"
        "resume_data": {
            "personalInfo": {...},
            "summary": "...",
            "experience": [...],
            "education": [...],
            "skills": [...]
        }
    }
    """
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Get resume from database
        resume = current_app.resume_model.get_resume_by_id(resume_id)
        if not resume:
            return jsonify({'error': 'Resume not found'}), 404
        
        # Verify ownership
        if str(resume['user_id']) != current_user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Get resume data from request or use stored data
        resume_data = data.get('resume_data')
        if not resume_data:
            # Build from stored data
            resume_data = {
                'personalInfo': {
                    'name': 'Candidate Name',
                    'email': resume.get('email'),
                    'phone': resume.get('phone'),
                    'linkedin': resume.get('linkedin')
                },
                'skills': resume.get('skills', []),
                'experience': [],
                'education': []
            }
        
        # Get template
        template = data.get('template', 'professional')
        
        # Generate PDF
        pdf_generator = ResumePDFGenerator(template=template)
        
        # Create output directory if doesn't exist
        output_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'pdfs', str(current_user_id))
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename
        filename = f"resume_{resume_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        output_path = os.path.join(output_dir, filename)
        
        # Generate PDF
        pdf_generator.generate_pdf(resume_data, output_path)
        
        # Send file
        return send_file(
            output_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"resume_{datetime.now().strftime('%Y%m%d')}.pdf"
        )
        
    except Exception as e:
        current_app.logger.error(f'PDF generation error: {str(e)}')
        return jsonify({'error': str(e)}), 500

@pdf_bp.route('/preview/<resume_id>', methods=['POST'])
@candidate_required
def preview_resume_pdf(resume_id):
    """Generate PDF preview (returns base64 encoded PDF)"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        resume = current_app.resume_model.get_resume_by_id(resume_id)
        if not resume or str(resume['user_id']) != current_user_id:
            return jsonify({'error': 'Resume not found'}), 404
        
        resume_data = data.get('resume_data', {})
        template = data.get('template', 'professional')
        
        # Generate PDF to buffer
        pdf_generator = ResumePDFGenerator(template=template)
        buffer = pdf_generator.generate_pdf(resume_data)
        
        # Encode to base64
        import base64
        pdf_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        return jsonify({
            'success': True,
            'pdf_base64': pdf_base64
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500