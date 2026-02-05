# backend/app/routes/resume_routes.py
from flask import Blueprint, request, jsonify, current_app
from app.utils.file_handler import save_uploaded_file
from bson import ObjectId
from app.services.resume_parser import parse_resume, extract_basic_info
<<<<<<< HEAD
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.decorators import candidate_required
=======
>>>>>>> b3a3b4bed96ef7f887abeaddc9d451e2b5943459

resume_bp = Blueprint('resume', __name__, url_prefix='/api/resume')

@resume_bp.route('/upload', methods=['POST'])
@candidate_required
def upload_resume():
<<<<<<< HEAD
    """Upload and parse resume file (Candidate only)"""
    try:
        current_user_id = get_jwt_identity()  # Get logged-in user ID
        
=======
    """Upload and parse resume file"""
    try:
>>>>>>> b3a3b4bed96ef7f887abeaddc9d451e2b5943459
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
<<<<<<< HEAD
        # Save file with current user's ID
        file_path = save_uploaded_file(file, current_user_id)
=======
        user_id = request.form.get('user_id', '000000000000000000000000')
        
        # Save file
        file_path = save_uploaded_file(file, user_id)
>>>>>>> b3a3b4bed96ef7f887abeaddc9d451e2b5943459
        if not file_path:
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Parse resume
        parsed_text = parse_resume(file_path)
        if not parsed_text:
            return jsonify({'error': 'Failed to parse resume'}), 500
        
        basic_info = extract_basic_info(parsed_text)
        
<<<<<<< HEAD
        # Extract skills
        from app.services.skill_extractor import SkillExtractor
        skill_extractor = SkillExtractor()
        skills = skill_extractor.extract_skills_with_ner(parsed_text)
        experience_years = skill_extractor.extract_experience_years(parsed_text)
        
=======
>>>>>>> b3a3b4bed96ef7f887abeaddc9d451e2b5943459
        # Save to database
        resume_id = current_app.resume_model.create_resume(
            user_id=current_user_id,
            filename=file.filename,
            file_path=file_path
        )
        
        # Update with parsed data
        current_app.resume_model.update_parsed_data(resume_id, {
            'parsed_text': parsed_text,
            'email': basic_info['email'],
            'phone': basic_info['phone'],
<<<<<<< HEAD
            'linkedin': basic_info['linkedin'],
            'skills': skills,
            'experience_years': experience_years
=======
            'linkedin': basic_info['linkedin']
>>>>>>> b3a3b4bed96ef7f887abeaddc9d451e2b5943459
        })
        
        return jsonify({
            'message': 'Resume uploaded and parsed successfully',
            'resume_id': resume_id,
            'filename': file.filename,
            'text_length': len(parsed_text),
<<<<<<< HEAD
            'skills_found': len(skills),
            'experience_years': experience_years,
=======
>>>>>>> b3a3b4bed96ef7f887abeaddc9d451e2b5943459
            'basic_info': basic_info
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@resume_bp.route('/my-resumes', methods=['GET'])
@candidate_required
def get_my_resumes():
    """Get all resumes for current user"""
    try:
        current_user_id = get_jwt_identity()
        resumes = current_app.resume_model.get_user_resumes(current_user_id)
        
        # Convert ObjectId to string
        for resume in resumes:
            resume['_id'] = str(resume['_id'])
            resume['user_id'] = str(resume['user_id'])
        
        return jsonify({
            'success': True,
            'count': len(resumes),
            'resumes': resumes
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@resume_bp.route('/<resume_id>/analyze-all-jobs', methods=['POST'])
@candidate_required
def analyze_against_all_jobs(resume_id):
    """Analyze resume against all active jobs"""
    try:
        current_user_id = get_jwt_identity()
        
        # Verify resume belongs to current user
        resume = current_app.resume_model.get_resume_by_id(resume_id)
        if not resume:
            return jsonify({'error': 'Resume not found'}), 404
        
        if str(resume['user_id']) != current_user_id:
            return jsonify({'error': 'Unauthorized access to resume'}), 403
        
        resume_text = resume.get('parsed_text', '')
        if not resume_text:
            return jsonify({'error': 'Resume not parsed'}), 400
        
        # Get all active jobs
        jobs = current_app.job_model.get_all_active_jobs()
        
        # Analyze against each job
        from app.services.ats_analyzer import ATSAnalyzer
        analyzer = ATSAnalyzer()
        results = []
        
        for job in jobs:
            job_text = job.get('description', '')
            if not job_text:
                continue
            
            analysis = analyzer.analyze_resume(resume_text, job_text)
            
            # Save match
            current_app.match_model.save_match(
                resume_id=resume_id,
                job_id=str(job['_id']),
                ats_score=analysis['ats_score'],
                skill_match_percentage=analysis['skill_match']['match_percentage'],
                missing_skills=analysis['skill_match']['missing_skills']
            )
            
            results.append({
                'job_id': str(job['_id']),
                'job_title': job.get('title'),
                'company': job.get('company', 'Not specified'),
                'location': job.get('location', 'Not specified'),
                'ats_score': analysis['ats_score'],
                'skill_match_percentage': analysis['skill_match']['match_percentage'],
                'matched_skills': analysis['skill_match']['matched_skills'][:10],
                'missing_skills': analysis['skill_match']['missing_skills'][:10],
                'experience_required': job.get('experience_required', 0),
                'recommendations': analysis['recommendations']
            })
        
        # Sort by ATS score
        results.sort(key=lambda x: x['ats_score'], reverse=True)
        
        return jsonify({
            'success': True,
            'resume_id': resume_id,
            'total_jobs_analyzed': len(results),
            'top_matches': results[:10],
            'all_matches': results
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500