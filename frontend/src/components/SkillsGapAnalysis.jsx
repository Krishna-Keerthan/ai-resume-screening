// frontend/src/components/SkillsGapAnalysis.jsx
import React, { useState, useEffect } from 'react';
import './SkillsGapAnalysis.css';

const SkillsGapAnalysis = ({ resumeSkills, jobMatches }) => {
    const [gapAnalysis, setGapAnalysis] = useState(null);

    useEffect(() => {
        analyzeSkillsGap();
    }, [resumeSkills, jobMatches]);

    const analyzeSkillsGap = () => {
        if (!jobMatches || jobMatches.length === 0) return;

        // Collect all missing skills across all jobs
        const allMissingSkills = {};
        
        jobMatches.forEach(job => {
            job.missing_skills.forEach(skill => {
                if (!allMissingSkills[skill]) {
                    allMissingSkills[skill] = {
                        count: 0,
                        jobs: []
                    };
                }
                allMissingSkills[skill].count++;
                allMissingSkills[skill].jobs.push(job.job_title);
            });
        });

        // Sort by frequency
        const sortedSkills = Object.entries(allMissingSkills)
            .map(([skill, data]) => ({
                skill,
                count: data.count,
                percentage: (data.count / jobMatches.length * 100).toFixed(1),
                jobs: data.jobs
            }))
            .sort((a, b) => b.count - a.count);

        // Categorize skills by priority
        const highPriority = sortedSkills.filter(s => s.count >= jobMatches.length * 0.5);
        const mediumPriority = sortedSkills.filter(s => s.count >= jobMatches.length * 0.25 && s.count < jobMatches.length * 0.5);
        const lowPriority = sortedSkills.filter(s => s.count < jobMatches.length * 0.25);

        setGapAnalysis({
            totalMissingSkills: sortedSkills.length,
            highPriority,
            mediumPriority,
            lowPriority,
            allSkills: sortedSkills
        });
    };

    if (!gapAnalysis) {
        return <div className="loading">Analyzing skills gap...</div>;
    }

    return (
        <div className="skills-gap-container">
            <div className="gap-header">
                <h2>Skills Gap Analysis</h2>
                <p>Based on {jobMatches.length} job matches</p>
            </div>

            <div className="gap-overview">
                <div className="overview-stat">
                    <div className="stat-value">{resumeSkills.length}</div>
                    <div className="stat-label">Your Skills</div>
                </div>
                <div className="overview-stat highlight">
                    <div className="stat-value">{gapAnalysis.totalMissingSkills}</div>
                    <div className="stat-label">Skills to Learn</div>
                </div>
                <div className="overview-stat">
                    <div className="stat-value">{gapAnalysis.highPriority.length}</div>
                    <div className="stat-label">High Priority</div>
                </div>
            </div>

            {gapAnalysis.highPriority.length > 0 && (
                <SkillPrioritySection
                    title="🔴 High Priority Skills"
                    subtitle="Required by 50%+ of jobs"
                    skills={gapAnalysis.highPriority}
                    color="high"
                />
            )}

            {gapAnalysis.mediumPriority.length > 0 && (
                <SkillPrioritySection
                    title="🟡 Medium Priority Skills"
                    subtitle="Required by 25-50% of jobs"
                    skills={gapAnalysis.mediumPriority}
                    color="medium"
                />
            )}

            {gapAnalysis.lowPriority.length > 0 && (
                <SkillPrioritySection
                    title="🟢 Low Priority Skills"
                    subtitle="Required by <25% of jobs"
                    skills={gapAnalysis.lowPriority}
                    color="low"
                />
            )}

            <LearningRecommendations skills={gapAnalysis.highPriority.slice(0, 5)} />
        </div>
    );
};

const SkillPrioritySection = ({ title, subtitle, skills, color }) => {
    return (
        <div className="priority-section">
            <h3>{title}</h3>
            <p className="subtitle">{subtitle}</p>
            <div className="skills-grid">
                {skills.map((skillData, idx) => (
                    <SkillGapCard key={idx} skillData={skillData} color={color} />
                ))}
            </div>
        </div>
    );
};

const SkillGapCard = ({ skillData, color }) => {
    const [showJobs, setShowJobs] = useState(false);

    return (
        <div className={`skill-gap-card ${color}`}>
            <div className="skill-header">
                <div className="skill-name">{skillData.skill}</div>
                <div className="skill-stats">
                    <span className="skill-count">{skillData.count} jobs</span>
                    <span className="skill-percentage">{skillData.percentage}%</span>
                </div>
            </div>
            
            <div className="progress-bar">
                <div 
                    className="progress-fill" 
                    style={{ width: `${skillData.percentage}%` }}
                ></div>
            </div>

            <button 
                className="show-jobs-btn"
                onClick={() => setShowJobs(!showJobs)}
            >
                {showJobs ? 'Hide' : 'Show'} Jobs ({skillData.jobs.length})
            </button>

            {showJobs && (
                <div className="jobs-list-mini">
                    {skillData.jobs.slice(0, 5).map((job, idx) => (
                        <div key={idx} className="job-item">{job}</div>
                    ))}
                    {skillData.jobs.length > 5 && (
                        <div className="job-item more">+{skillData.jobs.length - 5} more</div>
                    )}
                </div>
            )}
        </div>
    );
};

const LearningRecommendations = ({ skills }) => {
    const learningResources = {
        'python': 'https://www.python.org/about/gettingstarted/',
        'javascript': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript',
        'react': 'https://react.dev/learn',
        'nodejs': 'https://nodejs.org/en/learn/getting-started/introduction-to-nodejs',
        // Add more as needed
    };

    return (
        <div className="learning-recommendations">
            <h3>💡 Recommended Learning Path</h3>
            <p>Start with these high-impact skills to maximize your job opportunities</p>
            
            <div className="learning-path">
                {skills.slice(0, 5).map((skillData, idx) => (
                    <div key={idx} className="learning-step">
                        <div className="step-number">{idx + 1}</div>
                        <div className="step-content">
                            <h4>{skillData.skill}</h4>
                            <p>Required by {skillData.count} jobs ({skillData.percentage}%)</p>
                            {learningResources[skillData.skill.toLowerCase()] && (
                                <a 
                                    href={learningResources[skillData.skill.toLowerCase()]}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="learn-link"
                                >
                                    Start Learning →
                                </a>
                            )}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default SkillsGapAnalysis;