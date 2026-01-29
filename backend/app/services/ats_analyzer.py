# backend/app/services/ats_analyzer.py
from app.services.skill_extractor import SkillExtractor
from app.services.tfidf_service import TfidfService
from app.services.text_preprocessor import TextPreprocessor

class ATSAnalyzer:
    def __init__(self):
        self.skill_extractor = SkillExtractor()
        self.tfidf_service = TfidfService()
        self.preprocessor = TextPreprocessor()
    
    def analyze_resume(self, resume_text, job_description):
        """
        Complete ATS analysis of resume against job description
        
        Args:
            resume_text: Full resume text
            job_description: Full job description text
        
        Returns:
            Dictionary with complete analysis results
        """
        # Extract skills
        resume_skills = self.skill_extractor.extract_skills_with_ner(resume_text)
        job_skills = self.skill_extractor.extract_skills_with_ner(job_description)
        
        # Calculate skill match
        skill_match = self.skill_extractor.calculate_skill_match(resume_skills, job_skills)
        
        # Extract experience
        resume_experience = self.skill_extractor.extract_experience_years(resume_text)
        required_experience = self.skill_extractor.extract_experience_years(job_description)
        
        # Calculate TF-IDF similarity
        tfidf_score = self.tfidf_service.calculate_ats_score(resume_text, job_description)
        
        # Calculate weighted ATS score
        # 60% TF-IDF similarity + 40% skill match
        weighted_ats_score = (tfidf_score * 0.6) + (skill_match['match_percentage'] * 0.4)
        
        # Experience match
        experience_match = self._calculate_experience_match(resume_experience, required_experience)
        
        # Get top keywords from both
        resume_keywords = self.tfidf_service.get_top_keywords(resume_text, top_n=10)
        job_keywords = self.tfidf_service.get_top_keywords(job_description, top_n=10)
        
        # Generate analysis result
        result = {
            'ats_score': round(weighted_ats_score, 2),
            'tfidf_score': tfidf_score,
            'skill_match': skill_match,
            'resume_skills': resume_skills,
            'job_skills': job_skills,
            'experience': {
                'candidate': resume_experience,
                'required': required_experience,
                'match': experience_match
            },
            'resume_keywords': [kw[0] for kw in resume_keywords],
            'job_keywords': [kw[0] for kw in job_keywords],
            'recommendations': self._generate_recommendations(
                skill_match, 
                resume_experience, 
                required_experience,
                weighted_ats_score
            )
        }
        
        return result
    
    def _calculate_experience_match(self, resume_exp, required_exp):
        """Calculate if experience requirement is met"""
        if required_exp == 0:
            return {
                'meets_requirement': True,
                'message': 'No specific experience required'
            }
        
        meets_requirement = resume_exp >= required_exp
        
        return {
            'meets_requirement': meets_requirement,
            'gap_years': max(0, required_exp - resume_exp),
            'message': f"{'Meets' if meets_requirement else 'Does not meet'} experience requirement"
        }
    
    def _generate_recommendations(self, skill_match, resume_exp, required_exp, ats_score):
        """Generate recommendations for improving resume"""
        recommendations = []
        
        # Skill recommendations
        if skill_match['match_percentage'] < 50:
            recommendations.append({
                'type': 'critical',
                'category': 'skills',
                'message': f"Only {skill_match['match_percentage']}% skill match. Add these skills: {', '.join(skill_match['missing_skills'][:5])}"
            })
        elif skill_match['match_percentage'] < 75:
            recommendations.append({
                'type': 'warning',
                'category': 'skills',
                'message': f"Consider adding: {', '.join(skill_match['missing_skills'][:3])}"
            })
        
        # Experience recommendations
        if required_exp > 0 and resume_exp < required_exp:
            recommendations.append({
                'type': 'warning',
                'category': 'experience',
                'message': f"Job requires {required_exp} years, you have {resume_exp}. Highlight relevant projects."
            })
        
        # ATS score recommendations
        if ats_score < 60:
            recommendations.append({
                'type': 'critical',
                'category': 'content',
                'message': "Low ATS score. Use more keywords from job description in your resume."
            })
        elif ats_score < 75:
            recommendations.append({
                'type': 'info',
                'category': 'content',
                'message': "Good match. Consider optimizing resume format and adding more relevant details."
            })
        else:
            recommendations.append({
                'type': 'success',
                'category': 'content',
                'message': "Excellent match! Your resume aligns well with the job requirements."
            })
        
        return recommendations