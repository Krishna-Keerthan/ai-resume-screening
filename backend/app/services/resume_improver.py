# backend/app/services/resume_improver.py
from app.services.skill_extractor import SkillExtractor
from app.services.text_preprocessor import TextPreprocessor
import re

class ResumeImprover:
    def __init__(self):
        self.skill_extractor = SkillExtractor()
        self.preprocessor = TextPreprocessor()
    
    def generate_suggestions(self, resume_text, target_job=None):
        """
        Generate comprehensive suggestions for resume improvement
        
        Args:
            resume_text: Full resume text
            target_job: Optional job description to tailor suggestions
        
        Returns:
            Dictionary of categorized suggestions
        """
        suggestions = {
            'critical': [],
            'important': [],
            'optional': [],
            'formatting': [],
            'content': []
        }
        
        # Check resume length
        word_count = len(resume_text.split())
        if word_count < 300:
            suggestions['critical'].append({
                'issue': 'Resume too short',
                'suggestion': 'Expand your resume to at least 300-500 words. Add more details about your projects and achievements.',
                'impact': 'high'
            })
        elif word_count > 1000:
            suggestions['important'].append({
                'issue': 'Resume too long',
                'suggestion': 'Consider condensing to 600-800 words. Focus on most relevant experiences.',
                'impact': 'medium'
            })
        
        # Check for contact information
        if not re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', resume_text):
            suggestions['critical'].append({
                'issue': 'Missing email',
                'suggestion': 'Add your professional email address at the top of your resume.',
                'impact': 'high'
            })
        
        if not re.search(r'[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}', resume_text):
            suggestions['important'].append({
                'issue': 'Missing phone number',
                'suggestion': 'Include your phone number in the contact section.',
                'impact': 'medium'
            })
        
        # Check for LinkedIn
        if 'linkedin' not in resume_text.lower():
            suggestions['optional'].append({
                'issue': 'No LinkedIn profile',
                'suggestion': 'Add your LinkedIn profile URL to increase credibility.',
                'impact': 'low'
            })
        
        # Check for quantifiable achievements
        numbers = re.findall(r'\d+%|\d+\+|increased|decreased|improved|reduced', resume_text.lower())
        if len(numbers) < 3:
            suggestions['important'].append({
                'issue': 'Lack of quantifiable achievements',
                'suggestion': 'Add specific numbers and percentages to demonstrate impact (e.g., "Increased efficiency by 30%").',
                'impact': 'high'
            })
        
        # Check for action verbs
        weak_verbs = ['responsible for', 'worked on', 'helped with', 'assisted in']
        weak_verb_count = sum(1 for verb in weak_verbs if verb in resume_text.lower())
        if weak_verb_count > 2:
            suggestions['content'].append({
                'issue': 'Weak action verbs',
                'suggestion': 'Replace passive phrases with strong action verbs: "Developed", "Implemented", "Designed", "Led".',
                'impact': 'medium'
            })
        
        # Check sections
        required_sections = ['experience', 'education', 'skills']
        for section in required_sections:
            if section not in resume_text.lower():
                suggestions['critical'].append({
                    'issue': f'Missing {section.title()} section',
                    'suggestion': f'Add a dedicated {section.title()} section to your resume.',
                    'impact': 'high'
                })
        
        # Extract current skills
        current_skills = self.skill_extractor.extract_skills_with_ner(resume_text)
        
        # If target job provided, give tailored suggestions
        if target_job:
            job_skills = self.skill_extractor.extract_skills_with_ner(target_job)
            missing_skills = set(job_skills) - set(current_skills)
            
            if missing_skills:
                top_missing = list(missing_skills)[:5]
                suggestions['critical'].append({
                    'issue': 'Missing job-specific skills',
                    'suggestion': f'Add these skills if you have them: {", ".join(top_missing)}',
                    'impact': 'high',
                    'skills': top_missing
                })
        
        # Check for technical skills density
        if len(current_skills) < 5:
            suggestions['important'].append({
                'issue': 'Too few technical skills listed',
                'suggestion': 'List more technical skills and tools you\'ve worked with.',
                'impact': 'high'
            })
        
        # Formatting suggestions
        if '\t' in resume_text:
            suggestions['formatting'].append({
                'issue': 'Inconsistent formatting',
                'suggestion': 'Use consistent spacing instead of tabs.',
                'impact': 'low'
            })
        
        # Check for personal pronouns
        if re.search(r'\b(I|me|my|myself)\b', resume_text, re.IGNORECASE):
            suggestions['formatting'].append({
                'issue': 'First-person pronouns',
                'suggestion': 'Remove "I", "me", "my" - use bullet points with action verbs instead.',
                'impact': 'medium'
            })
        
        return suggestions
    
    def get_keyword_suggestions(self, resume_text, job_description):
        """Suggest keywords to add based on job description"""
        from app.services.tfidf_service import TfidfService
        
        tfidf = TfidfService()
        
        # Get top keywords from job
        job_keywords = tfidf.get_top_keywords(job_description, top_n=20)
        job_keyword_set = set([kw[0] for kw in job_keywords])
        
        # Get keywords from resume
        resume_keywords = tfidf.get_top_keywords(resume_text, top_n=20)
        resume_keyword_set = set([kw[0] for kw in resume_keywords])
        
        # Find missing keywords
        missing_keywords = job_keyword_set - resume_keyword_set
        
        return {
            'missing_keywords': list(missing_keywords)[:10],
            'job_keywords': [kw[0] for kw in job_keywords][:10],
            'resume_keywords': [kw[0] for kw in resume_keywords][:10]
        }
    
    def calculate_improvement_score(self, resume_text):
        """Calculate resume quality score (0-100)"""
        score = 100
        
        # Length check (20 points)
        word_count = len(resume_text.split())
        if word_count < 300:
            score -= 20
        elif word_count > 1000:
            score -= 10
        
        # Contact info (15 points)
        if not re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', resume_text):
            score -= 10
        if not re.search(r'[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}', resume_text):
            score -= 5
        
        # Skills (20 points)
        skills = self.skill_extractor.extract_skills_with_ner(resume_text)
        if len(skills) < 5:
            score -= 20
        elif len(skills) < 10:
            score -= 10
        
        # Quantifiable achievements (15 points)
        numbers = re.findall(r'\d+%|\d+\+|increased|decreased|improved|reduced', resume_text.lower())
        if len(numbers) < 3:
            score -= 15
        elif len(numbers) < 5:
            score -= 7
        
        # Required sections (20 points)
        required_sections = ['experience', 'education', 'skills']
        for section in required_sections:
            if section not in resume_text.lower():
                score -= 7
        
        # Action verbs (10 points)
        weak_verbs = ['responsible for', 'worked on', 'helped with', 'assisted in']
        weak_verb_count = sum(1 for verb in weak_verbs if verb in resume_text.lower())
        if weak_verb_count > 2:
            score -= 10
        
        return max(0, min(100, score))