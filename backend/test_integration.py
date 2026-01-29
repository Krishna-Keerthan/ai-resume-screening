# backend/test_integration.py
import pytest
from app import create_app
import json
from bson import ObjectId

@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["DEBUG"] = True
    app.config["PROPAGATE_EXCEPTIONS"] = True


    return app

@pytest.fixture
def client(app):
    return app.test_client()

class TestAuthentication:
    def test_register_candidate(self, client):
        """Test candidate registration"""
        response = client.post('/api/auth/register', 
            data=json.dumps({
                'email': 'test_candidate@example.com',
                'password': 'password123',
                'role': 'candidate'
            }),
            content_type='application/json'
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'access_token' in data
        assert data['role'] == 'candidate'
    
    def test_register_recruiter(self, client):
        """Test recruiter registration"""
        response = client.post('/api/auth/register',
            data=json.dumps({
                'email': 'test_recruiter@example.com',
                'password': 'password123',
                'role': 'recruiter'
            }),
            content_type='application/json'
        )
        assert response.status_code == 201
    
    def test_login(self, client):
        """Test login"""
        # First register
        client.post('/api/auth/register',
            data=json.dumps({
                'email': 'login_test@example.com',
                'password': 'password123',
                'role': 'candidate'
            }),
            content_type='application/json'
        )
        
        # Then login
        response = client.post('/api/auth/login',
            data=json.dumps({
                'email': 'login_test@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'access_token' in data

class TestResumeUpload:
    def test_upload_without_auth(self, client):
        """Test that upload requires authentication"""
        response = client.post('/api/resume/upload')
        assert response.status_code == 401
    
    def test_upload_with_auth(self, client):
        """Test resume upload with authentication"""
        # Register and login
        register_response = client.post('/api/auth/register',
            data=json.dumps({
                'email': 'upload_test@example.com',
                'password': 'password123',
                'role': 'candidate'
            }),
            content_type='application/json'
        )
        token = json.loads(register_response.data)['access_token']
        
        # Upload file (would need actual file here)
        # This is a placeholder for the test structure
        assert True

class TestJobOperations:
    def test_create_job_as_recruiter(self, client):
        """Test job creation by recruiter"""
        # Register recruiter
        register_response = client.post('/api/auth/register',
            data=json.dumps({
                'email': 'job_test_recruiter@example.com',
                'password': 'password123',
                'role': 'recruiter'
            }),
            content_type='application/json'
        )
        token = json.loads(register_response.data)['access_token']
        
        # Create job
        response = client.post('/api/jobs/create',
            headers={'Authorization': f'Bearer {token}'},
            data=json.dumps({
                'title': 'Test Job',
                'description': 'Test Description',
                'required_skills': ['python', 'flask'],
                'experience_required': 2
            }),
            content_type='application/json'
        )
        assert response.status_code == 201

# Run tests
if __name__ == '__main__':
    pytest.main([__file__, '-v'])