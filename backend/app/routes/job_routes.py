# backend/app/routes/job_routes.py
from flask import Blueprint, request, jsonify, current_app
from bson import ObjectId
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity


job_bp = Blueprint('job', __name__, url_prefix='/api/jobs')
#Something's wrong with JOB routes Check it for conflicts due to missing fields ['recruiters_id']
@job_bp.route('/create', methods=['POST'])
@jwt_required()
def create_job():
    try:
        data = request.get_json()
        recruiter_id = get_jwt_identity()  # 🔥 source of truth

        # Validate required fields (NO recruiter_id here)
        required_fields = ['title', 'description', 'required_skills']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400

        job_id = current_app.job_model.create_job(
            recruiter_id=recruiter_id,
            title=data['title'],
            description=data['description'],
            required_skills=data['required_skills'],
            experience_required=data.get('experience_required', 0)
        )

        current_app.db['jobs'].update_one(
            {'_id': ObjectId(job_id)},
            {'$set': {
                'location': data.get('location', 'Not specified'),
                'salary_range': data.get('salary_range', 'Not specified'),
                'employment_type': data.get('employment_type', 'Full-time'),
                'company': data.get('company', 'Not specified')
            }}
        )

        return jsonify({
            'message': 'Job created successfully',
            'job_id': job_id
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@job_bp.route('/all', methods=['GET'])
def get_all_jobs():
    """Get all active jobs"""
    try:
        jobs = current_app.job_model.get_all_active_jobs()
        
        # Convert ObjectId to string
        for job in jobs:
            job['_id'] = str(job['_id'])
            job['recruiter_id'] = str(job['recruiter_id'])
        
        return jsonify({
            'success': True,
            'count': len(jobs),
            'jobs': jobs
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@job_bp.route('/<job_id>', methods=['GET'])
def get_job(job_id):
    """Get job details by ID"""
    try:
        job = current_app.job_model.get_job_by_id(job_id)
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        job['_id'] = str(job['_id'])
        job['recruiter_id'] = str(job['recruiter_id'])
        
        return jsonify(job), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@job_bp.route('/<job_id>', methods=['PUT'])
def update_job(job_id):
    """Update job posting"""
    try:
        data = request.get_json()
        
        # Update job
        result = current_app.db['jobs'].update_one(
            {'_id': ObjectId(job_id)},
            {'$set': {
                **data,
                'updated_at': datetime.utcnow()
            }}
        )
        
        if result.matched_count == 0:
            return jsonify({'error': 'Job not found'}), 404
        
        return jsonify({'message': 'Job updated successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@job_bp.route('/<job_id>', methods=['DELETE'])
def delete_job(job_id):
    """Soft delete job (mark as inactive)"""
    try:
        result = current_app.db['jobs'].update_one(
            {'_id': ObjectId(job_id)},
            {'$set': {'is_active': False, 'deleted_at': datetime.utcnow()}}
        )
        
        if result.matched_count == 0:
            return jsonify({'error': 'Job not found'}), 404
        
        return jsonify({'message': 'Job deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@job_bp.route('/<job_id>/candidates', methods=['GET'])
def get_job_candidates(job_id):
    """Get all candidates who match this job"""
    try:
        matches = current_app.match_model.get_matches_for_job(job_id)
        
        # Get resume details for each match
        candidates = []
        for match in matches:
            resume = current_app.resume_model.get_resume_by_id(str(match['resume_id']))
            if resume:
                candidates.append({
                    'resume_id': str(match['resume_id']),
                    'filename': resume.get('filename'),
                    'email': resume.get('email'),
                    'ats_score': match['ats_score'],
                    'skill_match_percentage': match['skill_match_percentage'],
                    'missing_skills': match['missing_skills'],
                    'matched_at': match['matched_at']
                })
        
        return jsonify({
            'success': True,
            'job_id': job_id,
            'total_candidates': len(candidates),
            'candidates': candidates
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500