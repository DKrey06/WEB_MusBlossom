from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

def jwt_middleware():
    try:
        if request.method != 'OPTIONS':
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                verify_jwt_in_request()
        return None
    except Exception as e:
        if request.method == 'OPTIONS':
            return None
        if request.endpoint in ['api_login', 'api_register', 'api_refresh', 'api_categories', 
                                'api_articles', 'api_articles_detail', 'api_articles_by_category']:
            return None
        return jsonify({'success': False, 'error': str(e)}), 401

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user_id = get_jwt_identity()
        return fn(*args, **kwargs)
    return wrapper