// frontend/src/components/ResumeEditor.jsx
import React, { useState, useEffect } from 'react';
import './ResumeEditor.css';

const ResumeEditor = ({ resumeData, onSave }) => {
    const [editedData, setEditedData] = useState({
        personalInfo: {
            name: '',
            email: '',
            phone: '',
            linkedin: '',
            location: ''
        },
        summary: '',
        experience: [],
        education: [],
        skills: [],
        projects: []
    });

    const [activeSection, setActiveSection] = useState('personalInfo');

    useEffect(() => {
        if (resumeData) {
            // Parse resume data into editable format
            setEditedData({
                personalInfo: {
                    name: resumeData.name || '',
                    email: resumeData.email || '',
                    phone: resumeData.phone || '',
                    linkedin: resumeData.linkedin || '',
                    location: resumeData.location || ''
                },
                summary: resumeData.summary || '',
                experience: resumeData.experience || [],
                education: resumeData.education || [],
                skills: resumeData.skills || [],
                projects: resumeData.projects || []
            });
        }
    }, [resumeData]);

    const handlePersonalInfoChange = (field, value) => {
        setEditedData(prev => ({
            ...prev,
            personalInfo: {
                ...prev.personalInfo,
                [field]: value
            }
        }));
    };

    const handleSummaryChange = (value) => {
        setEditedData(prev => ({
            ...prev,
            summary: value
        }));
    };

    const addExperience = () => {
        setEditedData(prev => ({
            ...prev,
            experience: [
                ...prev.experience,
                {
                    id: Date.now(),
                    title: '',
                    company: '',
                    location: '',
                    startDate: '',
                    endDate: '',
                    current: false,
                    responsibilities: ['']
                }
            ]
        }));
    };

    const updateExperience = (id, field, value) => {
        setEditedData(prev => ({
            ...prev,
            experience: prev.experience.map(exp =>
                exp.id === id ? { ...exp, [field]: value } : exp
            )
        }));
    };

    const removeExperience = (id) => {
        setEditedData(prev => ({
            ...prev,
            experience: prev.experience.filter(exp => exp.id !== id)
        }));
    };

    const addEducation = () => {
        setEditedData(prev => ({
            ...prev,
            education: [
                ...prev.education,
                {
                    id: Date.now(),
                    degree: '',
                    field: '',
                    institution: '',
                    location: '',
                    graduationDate: '',
                    gpa: ''
                }
            ]
        }));
    };

    const updateEducation = (id, field, value) => {
        setEditedData(prev => ({
            ...prev,
            education: prev.education.map(edu =>
                edu.id === id ? { ...edu, [field]: value } : edu
            )
        }));
    };

    const removeEducation = (id) => {
        setEditedData(prev => ({
            ...prev,
            education: prev.education.filter(edu => edu.id !== id)
        }));
    };

    const addSkill = (skill) => {
        if (skill && !editedData.skills.includes(skill)) {
            setEditedData(prev => ({
                ...prev,
                skills: [...prev.skills, skill]
            }));
        }
    };

    const removeSkill = (skill) => {
        setEditedData(prev => ({
            ...prev,
            skills: prev.skills.filter(s => s !== skill)
        }));
    };

    const handleSave = () => {
        if (onSave) {
            onSave(editedData);
        }
    };

    return (
        <div className="resume-editor">
            <div className="editor-sidebar">
                <h3>Sections</h3>
                <button
                    className={activeSection === 'personalInfo' ? 'active' : ''}
                    onClick={() => setActiveSection('personalInfo')}
                >
                    Personal Info
                </button>
                <button
                    className={activeSection === 'summary' ? 'active' : ''}
                    onClick={() => setActiveSection('summary')}
                >
                    Summary
                </button>
                <button
                    className={activeSection === 'experience' ? 'active' : ''}
                    onClick={() => setActiveSection('experience')}
                >
                    Experience
                </button>
                <button
                    className={activeSection === 'education' ? 'active' : ''}
                    onClick={() => setActiveSection('education')}
                >
                    Education
                </button>
                <button
                    className={activeSection === 'skills' ? 'active' : ''}
                    onClick={() => setActiveSection('skills')}
                >
                    Skills
                </button>
            </div>

            <div className="editor-content">
                {activeSection === 'personalInfo' && (
                    <PersonalInfoSection
                        data={editedData.personalInfo}
                        onChange={handlePersonalInfoChange}
                    />
                )}

                {activeSection === 'summary' && (
                    <SummarySection
                        data={editedData.summary}
                        onChange={handleSummaryChange}
                    />
                )}

                {activeSection === 'experience' && (
                    <ExperienceSection
                        data={editedData.experience}
                        onAdd={addExperience}
                        onUpdate={updateExperience}
                        onRemove={removeExperience}
                    />
                )}

                {activeSection === 'education' && (
                    <EducationSection
                        data={editedData.education}
                        onAdd={addEducation}
                        onUpdate={updateEducation}
                        onRemove={removeEducation}
                    />
                )}

                {activeSection === 'skills' && (
                    <SkillsSection
                        data={editedData.skills}
                        onAdd={addSkill}
                        onRemove={removeSkill}
                    />
                )}
            </div>

            <div className="editor-actions">
                <button className="btn-save" onClick={handleSave}>
                    Save Changes
                </button>
                <button className="btn-preview">
                    Preview
                </button>
                <button className="btn-download">
                    Download PDF
                </button>
            </div>
        </div>
    );
};

const PersonalInfoSection = ({ data, onChange }) => {
    return (
        <div className="section-content">
            <h2>Personal Information</h2>
            
            <div className="form-group">
                <label>Full Name *</label>
                <input
                    type="text"
                    value={data.name}
                    onChange={(e) => onChange('name', e.target.value)}
                    placeholder="John Doe"
                />
            </div>

            <div className="form-row">
                <div className="form-group">
                    <label>Email *</label>
                    <input
                        type="email"
                        value={data.email}
                        onChange={(e) => onChange('email', e.target.value)}
                        placeholder="john@example.com"
                    />
                </div>

                <div className="form-group">
                    <label>Phone *</label>
                    <input
                        type="tel"
                        value={data.phone}
                        onChange={(e) => onChange('phone', e.target.value)}
                        placeholder="(123) 456-7890"
                    />
                </div>
            </div>

            <div className="form-group">
                <label>LinkedIn</label>
                <input
                    type="url"
                    value={data.linkedin}
                    onChange={(e) => onChange('linkedin', e.target.value)}
                    placeholder="linkedin.com/in/johndoe"
                />
            </div>

            <div className="form-group">
                <label>Location</label>
                <input
                    type="text"
                    value={data.location}
                    onChange={(e) => onChange('location', e.target.value)}
                    placeholder="City, State"
                />
            </div>
        </div>
    );
};

const SummarySection = ({ data, onChange }) => {
    const [charCount, setCharCount] = useState(data.length);

    const handleChange = (value) => {
        setCharCount(value.length);
        onChange(value);
    };

    return (
        <div className="section-content">
            <h2>Professional Summary</h2>
            <p className="section-tip">
                Write 2-3 sentences highlighting your key achievements and career goals
            </p>

            <div className="form-group">
                <textarea
                    value={data}
                    onChange={(e) => handleChange(e.target.value)}
                    placeholder="Experienced software engineer with 5+ years in full-stack development..."
                    rows="6"
                    maxLength="500"
                />
                <div className="char-count">{charCount}/500 characters</div>
            </div>

            <div className="ai-suggestions">
                <h4>💡 AI Suggestions</h4>
                <button className="suggestion-btn">Generate Summary</button>
            </div>
        </div>
    );
};

const ExperienceSection = ({ data, onAdd, onUpdate, onRemove }) => {
    return (
        <div className="section-content">
            <div className="section-header">
                <h2>Work Experience</h2>
                <button className="btn-add" onClick={onAdd}>+ Add Experience</button>
            </div>

            {data.length === 0 && (
                <div className="empty-state">
                    <p>No experience added yet. Click "Add Experience" to get started.</p>
                </div>
            )}

            {data.map((exp) => (
                <div key={exp.id} className="experience-item">
                    <div className="item-header">
                        <h3>Experience Entry</h3>
                        <button 
                            className="btn-remove"
                            onClick={() => onRemove(exp.id)}
                        >
                            Remove
                        </button>
                    </div>

                    <div className="form-group">
                        <label>Job Title *</label>
                        <input
                            type="text"
                            value={exp.title}
                            onChange={(e) => onUpdate(exp.id, 'title', e.target.value)}
                            placeholder="Software Engineer"
                        />
                    </div>

                    <div className="form-row">
                        <div className="form-group">
                            <label>Company *</label>
                            <input
                                type="text"
                                value={exp.company}
                                onChange={(e) => onUpdate(exp.id, 'company', e.target.value)}
                                placeholder="Tech Corp"
                            />
                        </div>

                        <div className="form-group">
                            <label>Location</label>
                            <input
                                type="text"
                                value={exp.location}
                                onChange={(e) => onUpdate(exp.id, 'location', e.target.value)}
                                placeholder="San Francisco, CA"
                            />
                        </div>
                    </div>

                    <div className="form-row">
                        <div className="form-group">
                            <label>Start Date *</label>
                            <input
                                type="month"
                                value={exp.startDate}
                                onChange={(e) => onUpdate(exp.id, 'startDate', e.target.value)}
                            />
                        </div>

                        <div className="form-group">
                            <label>End Date</label>
                            <input
                                type="month"
                                value={exp.endDate}
                                onChange={(e) => onUpdate(exp.id, 'endDate', e.target.value)}
                                disabled={exp.current}
                            />
                        </div>

                        <div className="form-group checkbox-group">
                            <label>
                                <input
                                    type="checkbox"
                                    checked={exp.current}
                                    onChange={(e) => onUpdate(exp.id, 'current', e.target.checked)}
                                />
                                Current Position
                            </label>
                        </div>
                    </div>

                    <div className="form-group">
                        <label>Key Responsibilities & Achievements</label>
                        <textarea
                            value={exp.responsibilities.join('\n')}
                            onChange={(e) => onUpdate(exp.id, 'responsibilities', e.target.value.split('\n'))}
                            placeholder="• Developed web applications using React&#10;• Led team of 5 engineers&#10;• Increased performance by 40%"
                            rows="5"
                        />
                        <div className="field-tip">
                            Use bullet points (start with •) and include metrics where possible
                        </div>
                    </div>
                </div>
            ))}
        </div>
    );
};

const EducationSection = ({ data, onAdd, onUpdate, onRemove }) => {
    return (
        <div className="section-content">
            <div className="section-header">
                <h2>Education</h2>
                <button className="btn-add" onClick={onAdd}>+ Add Education</button>
            </div>

            {data.length === 0 && (
                <div className="empty-state">
                    <p>No education added yet. Click "Add Education" to get started.</p>
                </div>
            )}

            {data.map((edu) => (
                <div key={edu.id} className="education-item">
                    <div className="item-header">
                        <h3>Education Entry</h3>
                        <button 
                            className="btn-remove"
                            onClick={() => onRemove(edu.id)}
                        >
                            Remove
                        </button>
                    </div>

                    <div className="form-row">
                        <div className="form-group">
                            <label>Degree *</label>
                            <input
                                type="text"
                                value={edu.degree}
                                onChange={(e) => onUpdate(edu.id, 'degree', e.target.value)}
                                placeholder="B.S., M.S., Ph.D., etc."
                            />
                        </div>

                        <div className="form-group">
                            <label>Field of Study *</label>
                            <input
                                type="text"
                                value={edu.field}
                                onChange={(e) => onUpdate(edu.id, 'field', e.target.value)}
                                placeholder="Computer Science"
                            />
                        </div>
                    </div>

                    <div className="form-group">
                        <label>Institution *</label>
                        <input
                            type="text"
                            value={edu.institution}
                            onChange={(e) => onUpdate(edu.id, 'institution', e.target.value)}
                            placeholder="University Name"
                        />
                    </div>

                    <div className="form-row">
                        <div className="form-group">
                            <label>Graduation Date</label>
                            <input
                                type="month"
                                value={edu.graduationDate}
                                onChange={(e) => onUpdate(edu.id, 'graduationDate', e.target.value)}
                            />
                        </div>

                        <div className="form-group">
                            <label>GPA (Optional)</label>
                            <input
                                type="text"
                                value={edu.gpa}
                                onChange={(e) => onUpdate(edu.id, 'gpa', e.target.value)}
                                placeholder="3.8/4.0"
                            />
                        </div>
                    </div>
                </div>
            ))}
        </div>
    );
};

const SkillsSection = ({ data, onAdd, onRemove }) => {
    const [newSkill, setNewSkill] = useState('');
    const [skillCategory, setSkillCategory] = useState('technical');

    const handleAddSkill = () => {
        if (newSkill.trim()) {
            onAdd(newSkill.trim());
            setNewSkill('');
        }
    };

    const suggestedSkills = [
        'Python', 'JavaScript', 'React', 'Node.js', 'MongoDB',
        'Docker', 'Kubernetes', 'AWS', 'Git', 'SQL'
    ];

    return (
        <div className="section-content">
            <h2>Skills</h2>

            <div className="skills-input">
                <div className="form-row">
                    <div className="form-group">
                        <input
                            type="text"
                            value={newSkill}
                            onChange={(e) => setNewSkill(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && handleAddSkill()}
                            placeholder="Add a skill (e.g., Python)"
                        />
                    </div>
                    <button className="btn-add-skill" onClick={handleAddSkill}>
                        Add Skill
                    </button>
                </div>
            </div>

            <div className="current-skills">
                <h4>Your Skills ({data.length})</h4>
                <div className="skills-list">
                    {data.map((skill, idx) => (
                        <div key={idx} className="skill-tag">
                            {skill}
                            <button 
                                className="remove-skill"
                                onClick={() => onRemove(skill)}
                            >
                                ×
                            </button>
                        </div>
                    ))}
                </div>
            </div>

            <div className="suggested-skills">
                <h4>💡 Suggested Skills</h4>
                <p>Click to add popular skills in your field</p>
                <div className="skills-list">
                    {suggestedSkills
                        .filter(skill => !data.includes(skill))
                        .map((skill, idx) => (
                            <div 
                                key={idx} 
                                className="skill-tag suggested"
                                onClick={() => onAdd(skill)}
                            >
                                {skill} +
                            </div>
                        ))}
                </div>
            </div>
        </div>
    );
};

export default ResumeEditor;