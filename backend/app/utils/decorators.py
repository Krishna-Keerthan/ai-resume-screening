# backend/app/utils/decorators.py
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request

def role_required(required_role):
    """
    Decorator to check if user has required role
    Usage: @role_required('recruiter')
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get('role')
            
            if user_role != required_role:
                return jsonify({
                    'error': 'Access forbidden',
                    'message': f'This endpoint requires {required_role} role'
                }), 403
            
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def candidate_required(fn):
    """Decorator for candidate-only routes"""
    return role_required('candidate')(fn)

def recruiter_required(fn):
    """Decorator for recruiter-only routes"""
    return role_required('recruiter')(fn)