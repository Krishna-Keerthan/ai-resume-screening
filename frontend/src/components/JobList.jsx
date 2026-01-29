// frontend/src/components/JobList.jsx
import React, { useState, useEffect } from 'react';
import { resumeAPI } from '../services/api';
import './JobList.css';

const JobList = ({ resumeId }) => {
    const [jobs, setJobs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [sortBy, setSortBy] = useState('ats_score'); // or 'skill_match'

    useEffect(() => {
        fetchJobMatches();
    }, [resumeId]);

    const fetchJobMatches = async () => {
        try {
            const response = await resumeAPI.analyzeAgainstAllJobs(resumeId);
            setJobs(response.data.all_matches || []);
        } catch (err) {
            setError('Failed to load job matches');
        } finally {
            setLoading(false);
        }
    };

    const sortJobs = (jobsArray) => {
        return [...jobsArray].sort((a, b) => {
            if (sortBy === 'ats_score') {
                return b.ats_score - a.ats_score;
            } else {
                return b.skill_match_percentage - a.skill_match_percentage;
            }
        });
    };

    const filterJobs = (threshold) => {
        return jobs.filter(job => job.ats_score >= threshold);
    };

    if (loading) return <div className="loading">Loading job matches...</div>;
    if (error) return <div className="error">{error}</div>;

    const sortedJobs = sortJobs(jobs);
    const excellentMatches = filterJobs(75);
    const goodMatches = filterJobs(50).filter(j => j.ats_score < 75);
    const needsImprovement = jobs.filter(j => j.ats_score < 50);

    return (
        <div className="job-list-container">
            <div className="list-header">
                <h2>Job Recommendations ({jobs.length})</h2>
                <div className="sort-controls">
                    <label>Sort by:</label>
                    <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
                        <option value="ats_score">ATS Score</option>
                        <option value="skill_match">Skill Match</option>
                    </select>
                </div>
            </div>

            <div className="match-summary">
                <div className="summary-card excellent">
                    <div className="count">{excellentMatches.length}</div>
                    <div className="label">Excellent Matches (75%+)</div>
                </div>
                <div className="summary-card good">
                    <div className="count">{goodMatches.length}</div>
                    <div className="label">Good Matches (50-74%)</div>
                </div>
                <div className="summary-card improvement">
                    <div className="count">{needsImprovement.length}</div>
                    <div className="label">Needs Improvement (&lt;50%)</div>
                </div>
            </div>

            {excellentMatches.length > 0 && (
                <JobSection title="🌟 Excellent Matches" jobs={excellentMatches} />
            )}

            {goodMatches.length > 0 && (
                <JobSection title="✅ Good Matches" jobs={goodMatches} />
            )}

            {needsImprovement.length > 0 && (
                <JobSection title="⚠️ Needs Improvement" jobs={needsImprovement} />
            )}
        </div>
    );
};

const JobSection = ({ title, jobs }) => {
    return (
        <div className="job-section">
            <h3>{title}</h3>
            <div className="jobs-list">
                {jobs.map((job, index) => (
                    <JobCard key={job.job_id} job={job} rank={index + 1} />
                ))}
            </div>
        </div>
    );
};

const JobCard = ({ job, rank }) => {
    const [expanded, setExpanded] = useState(false);

    return (
        <div className="job-card">
            <div className="job-card-main" onClick={() => setExpanded(!expanded)}>
                <div className="job-rank">#{rank}</div>
                <div className="job-details">
                    <h4>{job.job_title}</h4>
                    <p className="company">{job.company} • {job.location}</p>
                </div>
                <div className="job-scores">
                    <div className="score-badge ats">
                        <span className="score-value">{job.ats_score}</span>
                        <span className="score-label">ATS</span>
                    </div>
                    <div className="score-badge skill">
                        <span className="score-value">{job.skill_match_percentage}%</span>
                        <span className="score-label">Skills</span>
                    </div>
                </div>
                <div className="expand-icon">
                    {expanded ? '▲' : '▼'}
                </div>
            </div>

            {expanded && (
                <div className="job-card-details">
                    <div className="detail-section">
                        <h5>Matched Skills ({job.matched_skills.length})</h5>
                        <div className="skills-list">
                            {job.matched_skills.map((skill, idx) => (
                                <span key={idx} className="skill matched">{skill}</span>
                            ))}
                        </div>
                    </div>

                    {job.missing_skills.length > 0 && (
                        <div className="detail-section">
                            <h5>Missing Skills ({job.missing_skills.length})</h5>
                            <div className="skills-list">
                                {job.missing_skills.map((skill, idx) => (
                                    <span key={idx} className="skill missing">{skill}</span>
                                ))}
                            </div>
                        </div>
                    )}

                    <div className="detail-section">
                        <h5>Experience Required</h5>
                        <p>{job.experience_required}+ years</p>
                    </div>

                    {job.recommendations && job.recommendations.length > 0 && (
                        <div className="detail-section">
                            <h5>Recommendations</h5>
                            {job.recommendations.map((rec, idx) => (
                                <div key={idx} className={`rec ${rec.type}`}>
                                    {rec.message}
                                </div>
                            ))}
                        </div>
                    )}

                    <div className="action-buttons">
                        <button className="btn-apply">Apply Now</button>
                        <button className="btn-save">Save for Later</button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default JobList;