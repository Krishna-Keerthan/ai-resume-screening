# backend/app/routes/analysis_routes.py
from flask import Blueprint, request, jsonify, current_app
from app.services.ats_analyzer import ATSAnalyzer
from bson import ObjectId

analysis_bp = Blueprint('analysis', __name__, url_prefix='/api/analysis')

@analysis_bp.route('/analyze', methods=['POST'])
def analyze_resume():
    """
    Analyze resume against job description
    
    Request body:
    {
        "resume_id": "resume_id_here",
        "job_id": "job_id_here"
    }
    """
    try:
        data = request.get_json()
        resume_id = data.get('resume_id')
        job_id = data.get('job_id')
        
        if not resume_id or not job_id:
            return jsonify({'error': 'resume_id and job_id are required'}), 400
        
        # Get resume from database
        resume = current_app.resume_model.get_resume_by_id(resume_id)
        if not resume:
            return jsonify({'error': 'Resume not found'}), 404
        
        # Get job from database
        job = current_app.job_model.get_job_by_id(job_id)
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        # Get parsed text
        resume_text = resume.get('parsed_text', '')
        job_text = job.get('description', '')
        
        if not resume_text or not job_text:
            return jsonify({'error': 'Missing resume or job text'}), 400
        
        # Perform analysis
        analyzer = ATSAnalyzer()
        result = analyzer.analyze_resume(resume_text, job_text)
        
        # Save match to database
        current_app.match_model.save_match(
            resume_id=resume_id,
            job_id=job_id,
            ats_score=result['ats_score'],
            skill_match_percentage=result['skill_match']['match_percentage'],
            missing_skills=result['skill_match']['missing_skills']
        )
        
        return jsonify({
            'success': True,
            'analysis': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/batch-analyze/<resume_id>', methods=['POST'])
def batch_analyze(resume_id):
    """
    Analyze resume against all active jobs
    Returns top 10 matches
    """
    try:
        # Get resume
        resume = current_app.resume_model.get_resume_by_id(resume_id)
        if not resume:
            return jsonify({'error': 'Resume not found'}), 404
        
        resume_text = resume.get('parsed_text', '')
        if not resume_text:
            return jsonify({'error': 'Resume not parsed'}), 400
        
        # Get all active jobs
        jobs = current_app.job_model.get_all_active_jobs()
        
        # Analyze against each job
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
                'job_title': job.get('title', 'Unknown'),
                'ats_score': analysis['ats_score'],
                'skill_match_percentage': analysis['skill_match']['match_percentage'],
                'missing_skills': analysis['skill_match']['missing_skills'][:5]  # Top 5
            })
        
        # Sort by ATS score
        results.sort(key=lambda x: x['ats_score'], reverse=True)
        
        # Return top 10
        return jsonify({
            'success': True,
            'total_jobs_analyzed': len(results),
            'top_matches': results[:10]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500