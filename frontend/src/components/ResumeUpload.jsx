// frontend/src/components/ResumeUpload.jsx
import React, { useState } from 'react';
import { resumeAPI } from '../services/api';
import './ResumeUpload.css';

const ResumeUpload = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [message, setMessage] = useState('');
    const [resumeId, setResumeId] = useState(null);

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            // Validate file type
            const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
            if (!validTypes.includes(file.type)) {
                setMessage('Please upload a PDF or DOCX file');
                return;
            }
            // Validate file size (5MB)
            if (file.size > 5 * 1024 * 1024) {
                setMessage('File size must be less than 5MB');
                return;
            }
            setSelectedFile(file);
            setMessage('');
        }
    };

    const handleUpload = async () => {
        if (!selectedFile) {
            setMessage('Please select a file first');
            return;
        }

        setUploading(true);
        setMessage('');

        try {
            const response = await resumeAPI.uploadResume(selectedFile, '000000000000000000000000');
            setMessage('Resume uploaded successfully!');
            setResumeId(response.data.resume_id);
            console.log('Upload response:', response.data);
        } catch (error) {
            setMessage('Upload failed: ' + (error.response?.data?.error || error.message));
            console.error('Upload error:', error);
        } finally {
            setUploading(false);
        }
    };

    return (
        <div className="resume-upload-container">
            <h2>Upload Your Resume</h2>
            <div className="upload-section">
                <input
                    type="file"
                    accept=".pdf,.docx"
                    onChange={handleFileChange}
                    disabled={uploading}
                />
                {selectedFile && (
                    <p className="file-info">Selected: {selectedFile.name}</p>
                )}
                <button
                    onClick={handleUpload}
                    disabled={!selectedFile || uploading}
                    className="upload-button"
                >
                    {uploading ? 'Uploading...' : 'Upload Resume'}
                </button>
            </div>
            {message && (
                <p className={message.includes('success') ? 'success-message' : 'error-message'}>
                    {message}
                </p>
            )}
            {resumeId && (
                <div className="resume-id-info">
                    <p>Resume ID: {resumeId}</p>
                </div>
            )}
        </div>
    );
};

export default ResumeUpload;