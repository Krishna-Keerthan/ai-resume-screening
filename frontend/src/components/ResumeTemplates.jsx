// frontend/src/components/ResumeTemplates.jsx
import React, { useState } from 'react';
import './ResumeTemplates.css';

const ResumeTemplates = ({ resumeData, onTemplateSelect }) => {
    const [selectedTemplate, setSelectedTemplate] = useState('professional');

    const templates = [
        {
            id: 'professional',
            name: 'Professional',
            description: 'Clean and formal layout for corporate jobs',
            preview: '/templates/professional-preview.png',
            color: '#2c3e50'
        },
        {
            id: 'modern',
            name: 'Modern',
            description: 'Contemporary design with accent colors',
            preview: '/templates/modern-preview.png',
            color: '#3498db'
        },
        {
            id: 'creative',
            name: 'Creative',
            description: 'Bold design for creative industries',
            preview: '/templates/creative-preview.png',
            color: '#e74c3c'
        }
    ];

    const handleTemplateSelect = (templateId) => {
        setSelectedTemplate(templateId);
        if (onTemplateSelect) {
            onTemplateSelect(templateId);
        }
    };

    return (
        <div className="templates-container">
            <h2>Choose a Template</h2>
            <p className="subtitle">Select a template that matches your industry and style</p>

            <div className="templates-grid">
                {templates.map(template => (
                    <div
                        key={template.id}
                        className={`template-card ${selectedTemplate === template.id ? 'selected' : ''}`}
                        onClick={() => handleTemplateSelect(template.id)}
                    >
                        <div className="template-preview">
                            <div 
                                className="preview-placeholder"
                                style={{ borderColor: template.color }}
                            >
                                <span style={{ color: template.color }}>{template.name}</span>
                            </div>
                        </div>
                        <div className="template-info">
                            <h3>{template.name}</h3>
                            <p>{template.description}</p>
                        </div>
                        {selectedTemplate === template.id && (
                            <div className="selected-badge">✓ Selected</div>
                        )}
                    </div>
                ))}
            </div>

            {resumeData && (
                <div className="preview-section">
                    <h3>Preview</h3>
                    <ResumePreview data={resumeData} template={selectedTemplate} />
                </div>
            )}
        </div>
    );
};

const ResumePreview = ({ data, template }) => {
    const templateStyles = {
        professional: {
            headerBg: '#2c3e50',
            accentColor: '#3498db',
            fontFamily: 'Georgia, serif'
        },
        modern: {
            headerBg: '#3498db',
            accentColor: '#e74c3c',
            fontFamily: 'Arial, sans-serif'
        },
        creative: {
            headerBg: '#e74c3c',
            accentColor: '#f39c12',
            fontFamily: 'Helvetica, sans-serif'
        }
    };

    const style = templateStyles[template] || templateStyles.professional;

    return (
        <div className="resume-preview" style={{ fontFamily: style.fontFamily }}>
            <div className="preview-header" style={{ backgroundColor: style.headerBg }}>
                <h1>John Doe</h1>
                <p>{data?.email || 'email@example.com'} | {data?.phone || '(123) 456-7890'}</p>
            </div>

            <div className="preview-content">
                <section className="preview-section">
                    <h2 style={{ color: style.accentColor }}>Experience</h2>
                    <div className="preview-item">
                        <h3>Software Engineer</h3>
                        <p className="company">Tech Company | 2020 - Present</p>
                        <ul>
                            <li>Developed web applications using React and Node.js</li>
                            <li>Implemented RESTful APIs and microservices</li>
                        </ul>
                    </div>
                </section>

                <section className="preview-section">
                    <h2 style={{ color: style.accentColor }}>Skills</h2>
                    <div className="preview-skills">
                        {(data?.skills || ['Python', 'JavaScript', 'React', 'Node.js']).slice(0, 8).map((skill, idx) => (
                            <span key={idx} className="preview-skill" style={{ borderColor: style.accentColor }}>
                                {skill}
                            </span>
                        ))}
                    </div>
                </section>

                <section className="preview-section">
                    <h2 style={{ color: style.accentColor }}>Education</h2>
                    <div className="preview-item">
                        <h3>B.S. Computer Science</h3>
                        <p className="company">University Name | 2016 - 2020</p>
                    </div>
                </section>
            </div>
        </div>
    );
};

export default ResumeTemplates;