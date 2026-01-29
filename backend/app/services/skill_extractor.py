# backend/app/services/skill_extractor.py (update)
import spacy
from app.data.skills_database import ALL_SKILLS, SKILL_VARIATIONS
from app.services.text_preprocessor import TextPreprocessor
import re

class SkillExtractor:
    def __init__(self):
        self.all_skills = ALL_SKILLS
        self.skill_variations = SKILL_VARIATIONS
        self.preprocessor = TextPreprocessor()
        
        # Load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Downloading spaCy model...")
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")
    
    def extract_skills_with_ner(self, text):
        """
        Extract skills using spaCy Named Entity Recognition
        Combined with keyword matching for better accuracy
        """
        # Keyword-based extraction
        keyword_skills = self.extract_skills_keyword(text)
        
        # NER-based extraction
        doc = self.nlp(text)
        ner_skills = set()
        
        # Look for technical entities
        for ent in doc.ents:
            ent_text = ent.text.lower()
            # Check if entity matches known skills
            if ent_text in self.all_skills:
                ner_skills.add(ent_text)
        
        # Look for noun chunks that might be skills
        for chunk in doc.noun_chunks:
            chunk_text = chunk.text.lower()
            if chunk_text in self.all_skills:
                ner_skills.add(chunk_text)
        
        # Combine both methods
        all_skills = set(keyword_skills).union(ner_skills)
        
        return sorted(list(all_skills))
    
    def extract_skills_keyword(self, text):
        """Keyword-based skill extraction (previous method)"""
        text_lower = text.lower()
        found_skills = set()
        
        for skill in self.all_skills:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.add(skill)
        
        for variation, canonical in self.skill_variations.items():
            pattern = r'\b' + re.escape(variation) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.add(canonical)
        
        return sorted(list(found_skills))
    
    def extract_experience_years(self, text):
        """
        Extract years of experience from text
        Looks for patterns like "5 years", "3+ years", "2-4 years"
        """
        patterns = [
            r'(\d+)\+?\s*years?\s+(?:of\s+)?experience',
            r'experience\s+of\s+(\d+)\+?\s*years?',
            r'(\d+)\+?\s*yrs?\s+(?:of\s+)?experience'
        ]
        
        years = []
        text_lower = text.lower()
        
        for pattern in patterns:
            matches = re.findall(pattern, text_lower)
            years.extend([int(m) for m in matches])
        
        return max(years) if years else 0
    
    def calculate_skill_match(self, resume_skills, job_skills):
        """Calculate percentage match between resume and job skills"""
        resume_set = set(skill.lower() for skill in resume_skills)
        job_set = set(skill.lower() for skill in job_skills)
        
        if not job_set:
            return {
                'match_percentage': 0,
                'matched_skills': [],
                'missing_skills': []
            }
        
        matched = resume_set.intersection(job_set)
        missing = job_set - resume_set
        
        match_percentage = (len(matched) / len(job_set)) * 100
        
        return {
            'match_percentage': round(match_percentage, 2),
            'matched_skills': sorted(list(matched)),
            'missing_skills': sorted(list(missing))
        }