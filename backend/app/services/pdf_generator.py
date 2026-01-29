# backend/app/services/pdf_generator.py
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from io import BytesIO
from datetime import datetime

class ResumePDFGenerator:
    def __init__(self, template='professional'):
        self.template = template
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Header style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subheader style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#7f8c8d'),
            spaceAfter=12,
            alignment=TA_CENTER
        ))
        
        # Section header
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=8,
            spaceBefore=12,
            fontName='Helvetica-Bold',
            borderWidth=1,
            borderColor=colors.HexColor('#4CAF50'),
            borderPadding=5,
            backColor=colors.HexColor('#f8f9fa')
        ))
        
        # Job title style
        self.styles.add(ParagraphStyle(
            name='JobTitle',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#2c3e50'),
            fontName='Helvetica-Bold',
            spaceAfter=2
        ))
        
        # Company style
        self.styles.add(ParagraphStyle(
            name='Company',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#7f8c8d'),
            spaceAfter=4
        ))
        
        # Body text
        self.styles.add(ParagraphStyle(
            name='BodyText',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#333333'),
            spaceAfter=6,
            alignment=TA_JUSTIFY
        ))
    
    def generate_pdf(self, resume_data, output_path=None):
        """
        Generate PDF from resume data
        
        Args:
            resume_data: Dictionary containing resume information
            output_path: Optional file path to save PDF
        
        Returns:
            BytesIO buffer or file path
        """
        # Create buffer or file
        if output_path:
            buffer = output_path
        else:
            buffer = BytesIO()
        
        # Create PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Build content
        story = []
        
        # Personal Info
        story.extend(self._build_header(resume_data.get('personalInfo', {})))
        
        # Summary
        if resume_data.get('summary'):
            story.extend(self._build_summary(resume_data['summary']))
        
        # Experience
        if resume_data.get('experience'):
            story.extend(self._build_experience(resume_data['experience']))
        
        # Education
        if resume_data.get('education'):
            story.extend(self._build_education(resume_data['education']))
        
        # Skills
        if resume_data.get('skills'):
            story.extend(self._build_skills(resume_data['skills']))
        
        # Projects (if any)
        if resume_data.get('projects'):
            story.extend(self._build_projects(resume_data['projects']))
        
        # Build PDF
        doc.build(story)
        
        if not output_path:
            buffer.seek(0)
            return buffer
        
        return output_path
    
    def _build_header(self, personal_info):
        """Build header section with contact info"""
        story = []
        
        # Name
        name = personal_info.get('name', 'Your Name')
        story.append(Paragraph(name, self.styles['CustomTitle']))
        
        # Contact info
        contact_parts = []
        if personal_info.get('email'):
            contact_parts.append(personal_info['email'])
        if personal_info.get('phone'):
            contact_parts.append(personal_info['phone'])
        if personal_info.get('location'):
            contact_parts.append(personal_info['location'])
        if personal_info.get('linkedin'):
            contact_parts.append(personal_info['linkedin'])
        
        if contact_parts:
            contact_line = ' • '.join(contact_parts)
            story.append(Paragraph(contact_line, self.styles['CustomSubtitle']))
        
        story.append(Spacer(1, 0.2*inch))
        
        return story
    
    def _build_summary(self, summary):
        """Build professional summary section"""
        story = []
        
        story.append(Paragraph('PROFESSIONAL SUMMARY', self.styles['SectionHeader']))
        story.append(Paragraph(summary, self.styles['BodyText']))
        story.append(Spacer(1, 0.15*inch))
        
        return story
    
    def _build_experience(self, experiences):
        """Build work experience section"""
        story = []
        
        story.append(Paragraph('WORK EXPERIENCE', self.styles['SectionHeader']))
        
        for exp in experiences:
            # Job title and dates
            title = exp.get('title', 'Position')
            company = exp.get('company', 'Company')
            location = exp.get('location', '')
            start_date = exp.get('startDate', '')
            end_date = exp.get('endDate', 'Present') if not exp.get('current') else 'Present'
            
            # Format dates
            if start_date:
                try:
                    start_date = datetime.strptime(start_date, '%Y-%m').strftime('%B %Y')
                except:
                    pass
            if end_date and end_date != 'Present':
                try:
                    end_date = datetime.strptime(end_date, '%Y-%m').strftime('%B %Y')
                except:
                    pass
            
            story.append(Paragraph(title, self.styles['JobTitle']))
            
            company_line = f"{company}"
            if location:
                company_line += f" • {location}"
            if start_date:
                company_line += f" • {start_date} - {end_date}"
            
            story.append(Paragraph(company_line, self.styles['Company']))
            
            # Responsibilities
            responsibilities = exp.get('responsibilities', [])
            if isinstance(responsibilities, list):
                for resp in responsibilities:
                    if resp.strip():
                        bullet_text = f"• {resp.strip()}"
                        story.append(Paragraph(bullet_text, self.styles['BodyText']))
            
            story.append(Spacer(1, 0.1*inch))
        
        return story
    
    def _build_education(self, education_list):
        """Build education section"""
        story = []
        
        story.append(Paragraph('EDUCATION', self.styles['SectionHeader']))
        
        for edu in education_list:
            degree = edu.get('degree', '')
            field = edu.get('field', '')
            institution = edu.get('institution', '')
            grad_date = edu.get('graduationDate', '')
            gpa = edu.get('gpa', '')
            
            # Format degree line
            degree_line = f"{degree}"
            if field:
                degree_line += f" in {field}"
            story.append(Paragraph(degree_line, self.styles['JobTitle']))
            
            # Institution line
            inst_line = institution
            if grad_date:
                try:
                    grad_date = datetime.strptime(grad_date, '%Y-%m').strftime('%B %Y')
                    inst_line += f" • Graduated {grad_date}"
                except:
                    inst_line += f" • {grad_date}"
            if gpa:
                inst_line += f" • GPA: {gpa}"
            
            story.append(Paragraph(inst_line, self.styles['Company']))
            story.append(Spacer(1, 0.1*inch))
        
        return story
    
    def _build_skills(self, skills):
        """Build skills section"""
        story = []
        
        story.append(Paragraph('SKILLS', self.styles['SectionHeader']))
        
        # Group skills into rows for better formatting
        skills_text = ', '.join(skills)
        story.append(Paragraph(skills_text, self.styles['BodyText']))
        story.append(Spacer(1, 0.15*inch))
        
        return story
    
    def _build_projects(self, projects):
        """Build projects section"""
        story = []
        
        story.append(Paragraph('PROJECTS', self.styles['SectionHeader']))
        
        for project in projects:
            name = project.get('name', 'Project')
            description = project.get('description', '')
            technologies = project.get('technologies', [])
            
            story.append(Paragraph(name, self.styles['JobTitle']))
            
            if description:
                story.append(Paragraph(description, self.styles['BodyText']))
            
            if technologies:
                tech_text = f"Technologies: {', '.join(technologies)}"
                story.append(Paragraph(tech_text, self.styles['Company']))
            
            story.append(Spacer(1, 0.1*inch))
        
        return story