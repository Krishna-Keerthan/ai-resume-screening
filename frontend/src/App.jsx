// frontend/src/App.js
import React from 'react';
import ResumeUpload from './components/ResumeUpload';
import './App.css';

function App() {
    return (
        <div className="App">
            <header className="App-header">
                <h1>AI Resume Screening System</h1>
                <p>Upload your resume to get matched with jobs</p>
            </header>
            <main>
                <ResumeUpload />
            </main>
        </div>
    );
}

export default App;