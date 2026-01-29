# backend/app/routes/auth_routes.py
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token,
    jwt_required, 
    get_jwt_identity,
    get_jwt
)
from datetime import datetime
import re

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    return True, "Valid"

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    
    Request body:
    {
        "email": "user@example.com",
        "password": "password123",
        "role": "candidate"  // or "recruiter"
    }
    """
    try:
        data = request.get_json()
        
        # Validate input
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        email = data['email'].lower().strip()
        password = data['password']
        role = data.get('role', 'candidate')
        
        # Validate email
        if not validate_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate password
        is_valid, message = validate_password(password)
        if not is_valid:
            return jsonify({'error': message}), 400
        
        # Validate role
        if role not in ['candidate', 'recruiter']:
            return jsonify({'error': 'Role must be candidate or recruiter'}), 400
        
        # Check if user already exists
        existing_user = current_app.user_model.find_by_email(email)
        if existing_user:
            return jsonify({'error': 'Email already registered'}), 409
        
        # Create user
        user_id = current_app.user_model.create_user(email, password, role)
        
        # Create tokens
        access_token = create_access_token(identity=user_id, additional_claims={'role': role})
        refresh_token = create_refresh_token(identity=user_id, additional_claims={'role': role})
        
        return jsonify({
            'message': 'User registered successfully',
            'user_id': user_id,
            'email': email,
            'role': role,
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user
    
    Request body:
    {
        "email": "user@example.com",
        "password": "password123"
    }
    """
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        email = data['email'].lower().strip()
        password = data['password']
        
        # Find user
        user = current_app.user_model.find_by_email(email)
        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Verify password
        if not current_app.user_model.verify_password(user, password):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Create tokens
        user_id = str(user['_id'])
        role = user['role']
        
        access_token = create_access_token(identity=user_id, additional_claims={'role': role})
        refresh_token = create_refresh_token(identity=user_id, additional_claims={'role': role})
        
        # Update last login
        current_app.db['users'].update_one(
            {'_id': user['_id']},
            {'$set': {'last_login': datetime.utcnow()}}
        )
        
        return jsonify({
            'message': 'Login successful',
            'user_id': user_id,
            'email': email,
            'role': role,
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Get new access token using refresh token"""
    try:
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        role = claims.get('role', 'candidate')
        
        new_access_token = create_access_token(
            identity=current_user_id,
            additional_claims={'role': role}
        )
        
        return jsonify({
            'access_token': new_access_token
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user information"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get user from database
        from bson import ObjectId
        user = current_app.db['users'].find_one({'_id': ObjectId(current_user_id)})
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user_id': str(user['_id']),
            'email': user['email'],
            'role': user['role'],
            'created_at': user['created_at']
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change user password"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        
        if not old_password or not new_password:
            return jsonify({'error': 'Old and new passwords are required'}), 400
        
        # Validate new password
        is_valid, message = validate_password(new_password)
        if not is_valid:
            return jsonify({'error': message}), 400
        
        # Get user
        from bson import ObjectId
        user = current_app.db['users'].find_one({'_id': ObjectId(current_user_id)})
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Verify old password
        if not current_app.user_model.verify_password(user, old_password):
            return jsonify({'error': 'Incorrect old password'}), 401
        
        # Update password
        from werkzeug.security import generate_password_hash
        current_app.db['users'].update_one(
            {'_id': ObjectId(current_user_id)},
            {'$set': {
                'password_hash': generate_password_hash(new_password),
                'password_changed_at': datetime.utcnow()
            }}
        )
        
        return jsonify({'message': 'Password changed successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500