// frontend/src/services/api.js
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// frontend/src/services/api.js (update)
export const resumeAPI = {
    uploadResume: (file) => {
        const formData = new FormData();
        formData.append('file', file);
        
        const token = localStorage.getItem('access_token');
        return api.post('/resume/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
                'Authorization': `Bearer ${token}`
            },
        });
    },
    
    getMyResumes: () => {
        const token = localStorage.getItem('access_token');
        return api.get('/resume/my-resumes', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
    },
    
    analyzeAgainstAllJobs: (resumeId) => {
        const token = localStorage.getItem('access_token');
        return api.post(`/resume/${resumeId}/analyze-all-jobs`, {}, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
    },
};

export const authAPI = {
    register: (email, password, role) => {
        return api.post('/auth/register', { email, password, role });
    },
    
    login: (email, password) => {
        return api.post('/auth/login', { email, password });
    },
    
    getCurrentUser: () => {
        const token = localStorage.getItem('access_token');
        return api.get('/auth/me', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
    }
};

// frontend/src/services/api.js (update)
api.interceptors.response.use(
    response => response,
    error => {
        if (error.response) {
            // Server responded with error
            console.error('API Error:', error.response.data);
        } else if (error.request) {
            // No response received
            console.error('Network Error:', error.message);
        }
        return Promise.reject(error);
    }
);

export const pdfAPI = {
    generatePDF: (resumeId, resumeData, template = 'professional') => {
        const token = localStorage.getItem('access_token');
        return api.post(`/pdf/generate/${resumeId}`, 
            { resume_data: resumeData, template },
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                responseType: 'blob' // Important for file download
            }
        );
    },
    
    previewPDF: (resumeId, resumeData, template = 'professional') => {
        const token = localStorage.getItem('access_token');
        return api.post(`/pdf/preview/${resumeId}`,
            { resume_data: resumeData, template },
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            }
        );
    }
};

export default api;