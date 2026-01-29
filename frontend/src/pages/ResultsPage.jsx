// frontend/src/pages/ResultsPage.jsx
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { resumeAPI } from '../services/api';
import './ResultsPage.css';

const ResultsPage = () => {
    const { resumeId } = useParams();
    const [loading, setLoading] = useState(true);
    const [results, setResults] = useState(null);
    const [error, setError] = useState('');

    useEffect(() => {
        analyzeResume();
    }, [resumeId]);

    const analyzeResume = async () => {
        setLoading(true);
        setError('');
        
        try {
            const response = await resumeAPI.analyzeAgainstAllJobs(resumeId);
            setResults(response.data);
        } catch (err) {
            setError('Failed to analyze resume: ' + (err.response?.data?.error || err.message));
        } finally {
            setLoading(false);
        }
    };

    const getScoreColor = (score) => {
        if (score >= 75) return '#4CAF50'; // Green
        if (score >= 50) return '#FF9800'; // Orange
        return '#f44336'; // Red
    };

    const getScoreLabel = (score) => {
        if (score >= 75) return 'Excellent Match';
        if (score >= 50) return 'Good Match';
        return 'Needs Improvement';
    };

    if (loading) {
        return (
            <div className="results-container">
                <div className="loading">
                    <div className="spinner"></div>
                    <p>Analyzing your resume against all jobs...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="results-container">
                <div className="error-box">
                    <h3>Error</h3>
                    <p>{error}</p>
                    <button onClick={analyzeResume}>Try Again</button>
                </div>
            </div>
        );
    }

    if (!results || !results.top_matches || results.top_matches.length === 0) {
        return (
            <div className="results-container">
                <div className="no-results">
                    <h3>No Matching Jobs Found</h3>
                    <p>We couldn't find any jobs matching your resume at this time.</p>
                </div>
            </div>
        );
    }

    return (
        <div className="results-container">
            <div className="results-header">
                <h1>Resume Analysis Results</h1>
                <p>Found {results.total_jobs_analyzed} matching opportunities</p>
            </div>

            <div className="top-match-highlight">
                <h2>🎯 Best Match</h2>
                <JobMatchCard job={results.top_matches[0]} rank={1} />
            </div>

            <div className="all-matches">
                <h2>All Matches</h2>
                <div className="matches-grid">
                    {results.top_matches.slice(1).map((job, index) => (
                        <JobMatchCard key={job.job_id} job={job} rank={index + 2} />
                    ))}
                </div>
            </div>
        </div>
    );
};

const JobMatchCard = ({ job, rank }) => {
    const getScoreColor = (score) => {
        if (score >= 75) return '#4CAF50';
        if (score >= 50) return '#FF9800';
        return '#f44336';
    };

    return (
        <div className="job-match-card">
            <div className="card-header">
                <div className="rank-badge">#{rank}</div>
                <div className="job-info">
                    <h3>{job.job_title}</h3>
                    <p className="company">{job.company}</p>
                    <p className="location">{job.location}</p>
                </div>
            </div>

            <div className="score-section">
                <div className="score-circle" style={{ borderColor: getScoreColor(job.ats_score) }}>
                    <div className="score-value" style={{ color: getScoreColor(job.ats_score) }}>
                        {job.ats_score}
                    </div>
                    <div className="score-label">ATS Score</div>
                </div>
                <div className="skill-match">
                    <div className="match-percentage">
                        {job.skill_match_percentage}% Skill Match
                    </div>
                    <div className="experience-info">
                        {job.experience_required > 0 && (
                            <span>{job.experience_required}+ years required</span>
                        )}
                    </div>
                </div>
            </div>

            <div className="skills-section">
                <div className="matched-skills">
                    <h4>✓ Matched Skills ({job.matched_skills.length})</h4>
                    <div className="skills-tags">
                        {job.matched_skills.slice(0, 5).map((skill, idx) => (
                            <span key={idx} className="skill-tag matched">{skill}</span>
                        ))}
                        {job.matched_skills.length > 5 && (
                            <span className="skill-tag more">+{job.matched_skills.length - 5} more</span>
                        )}
                    </div>
                </div>

                {job.missing_skills.length > 0 && (
                    <div className="missing-skills">
                        <h4>⚠ Missing Skills ({job.missing_skills.length})</h4>
                        <div className="skills-tags">
                            {job.missing_skills.slice(0, 5).map((skill, idx) => (
                                <span key={idx} className="skill-tag missing">{skill}</span>
                            ))}
                            {job.missing_skills.length > 5 && (
                                <span className="skill-tag more">+{job.missing_skills.length - 5} more</span>
                            )}
                        </div>
                    </div>
                )}
            </div>

            {job.recommendations && job.recommendations.length > 0 && (
                <div className="recommendations">
                    <h4>💡 Recommendations</h4>
                    {job.recommendations.map((rec, idx) => (
                        <div key={idx} className={`recommendation ${rec.type}`}>
                            {rec.message}
                        </div>
                    ))}
                </div>
            )}

            <div className="card-actions">
                <button className="btn-primary">View Full Details</button>
                <button className="btn-secondary">Apply Now</button>
            </div>
        </div>
    );
};

export default ResultsPage;