# backend/app/utils/error_handler.py
from flask import jsonify
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):
    """Register global error handlers"""
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        """Handle HTTP exceptions"""
        return jsonify({
            'error': e.name,
            'message': e.description
        }), e.code
    
    @app.errorhandler(500)
    def handle_internal_error(e):
        """Handle internal server errors"""
        app.logger.error(f'Internal error: {str(e)}')
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred'
        }), 500
    
    @app.errorhandler(404)
    def handle_not_found(e):
        """Handle not found errors"""
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found'
        }), 404
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        """Handle all other exceptions"""
        app.logger.error(f'Unhandled exception: {str(e)}')
        return jsonify({
            'error': 'Server Error',
            'message': str(e)
        }), 500