# backend/app/routes/improvement_routes.py
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.decorators import candidate_required
from app.services.resume_improver import ResumeImprover
from bson import ObjectId

improvement_bp = Blueprint('improvement', __name__, url_prefix='/api/improvement')

@improvement_bp.route('/analyze/<resume_id>', methods=['POST'])
@candidate_required
def analyze_resume_quality(resume_id):
    """
    Analyze resume and provide improvement suggestions
    
    Optional body:
    {
        "job_id": "optional_job_id_for_tailored_suggestions"
    }
    """
    try:
        current_user_id = get_jwt_identity()
        
        # Get resume
        resume = current_app.resume_model.get_resume_by_id(resume_id)
        if not resume:
            return jsonify({'error': 'Resume not found'}), 404
        
        # Verify ownership
        if str(resume['user_id']) != current_user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        resume_text = resume.get('parsed_text', '')
        if not resume_text:
            return jsonify({'error': 'Resume not parsed'}), 400
        
        # Get optional job for tailored suggestions
        job_text = None
        data = request.get_json() or {}
        job_id = data.get('job_id')
        
        if job_id:
            job = current_app.job_model.get_job_by_id(job_id)
            if job:
                job_text = job.get('description', '')
        
        # Generate suggestions
        improver = ResumeImprover()
        suggestions = improver.generate_suggestions(resume_text, job_text)
        quality_score = improver.calculate_improvement_score(resume_text)
        
        # Get keyword suggestions if job provided
        keyword_suggestions = None
        if job_text:
            keyword_suggestions = improver.get_keyword_suggestions(resume_text, job_text)
        
        return jsonify({
            'success': True,
            'quality_score': quality_score,
            'suggestions': suggestions,
            'keyword_suggestions': keyword_suggestions,
            'total_suggestions': sum(len(v) for v in suggestions.values())
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@improvement_bp.route('/quick-tips', methods=['GET'])
@jwt_required()
def get_quick_tips():
    """Get general resume writing tips"""
    tips = [
        {
            'category': 'Content',
            'tips': [
                'Use strong action verbs: Developed, Implemented, Led, Designed',
                'Quantify achievements with numbers and percentages',
                'Focus on results and impact, not just responsibilities',
                'Tailor your resume to each job application'
            ]
        },
        {
            'category': 'Formatting',
            'tips': [
                'Keep it to 1-2 pages maximum',
                'Use consistent font sizes and spacing',
                'Avoid using first-person pronouns (I, me, my)',
                'Use bullet points for easy scanning'
            ]
        },
        {
            'category': 'Skills',
            'tips': [
                'List both technical and soft skills',
                'Include specific tools and technologies',
                'Match skills to job requirements',
                'Group similar skills together'
            ]
        },
        {
            'category': 'ATS Optimization',
            'tips': [
                'Use standard section headings (Experience, Education, Skills)',
                'Include keywords from job description',
                'Avoid complex formatting, tables, and graphics',
                'Use both acronyms and full terms (ML and Machine Learning)'
            ]
        }
    ]
    
    return jsonify({'tips': tips}), 200

@improvement_bp.route('/compare-versions', methods=['POST'])
@candidate_required
def compare_resume_versions():
    """
    Compare two versions of resume
    
    Request body:
    {
        "original_resume_id": "id1",
        "updated_resume_id": "id2"
    }
    """
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        original_id = data.get('original_resume_id')
        updated_id = data.get('updated_resume_id')
        
        if not original_id or not updated_id:
            return jsonify({'error': 'Both resume IDs required'}), 400
        
        # Get both resumes
        original = current_app.resume_model.get_resume_by_id(original_id)
        updated = current_app.resume_model.get_resume_by_id(updated_id)
        
        if not original or not updated:
            return jsonify({'error': 'Resume not found'}), 404
        
        # Verify ownership
        if str(original['user_id']) != current_user_id or str(updated['user_id']) != current_user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Calculate scores for both
        improver = ResumeImprover()
        original_score = improver.calculate_improvement_score(original.get('parsed_text', ''))
        updated_score = improver.calculate_improvement_score(updated.get('parsed_text', ''))
        
        # Compare skills
        original_skills = set(original.get('skills', []))
        updated_skills = set(updated.get('skills', []))
        
        added_skills = list(updated_skills - original_skills)
        removed_skills = list(original_skills - updated_skills)
        
        return jsonify({
            'success': True,
            'comparison': {
                'original_score': original_score,
                'updated_score': updated_score,
                'improvement': updated_score - original_score,
                'skills_added': added_skills,
                'skills_removed': removed_skills,
                'word_count_change': len(updated.get('parsed_text', '').split()) - len(original.get('parsed_text', '').split())
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500