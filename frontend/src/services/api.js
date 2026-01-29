// frontend/src/services/api.js
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const resumeAPI = {
    uploadResume: (file, userId) => {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('user_id', userId);
        
        return api.post('/resume/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
    },
    
    getResume: (resumeId) => {
        return api.get(`/resume/${resumeId}`);
    },
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

export default api;