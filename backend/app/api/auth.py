"""
Authentication API
User login and signup
Refactored to use OOP Controllers
"""
from flask import Blueprint


bp = Blueprint('auth', __name__)

# Need to expose token_required for other modules to import
# Re-exporting it from here for backward compatibility or move it to a util
# Better to move token_required to a shared decorator file, but that's a larger refactor.
# For now, let's keep it here but adapt since we moved logic to controller.
# Wait, token_required is used by decorators. We need to keep it available.
# Let's import it from a new location or keep it here.
# Actually, I should extract token_required to a utility to avoid circular imports.

from functools import wraps
from flask import request, jsonify
import jwt
from app.models.user import User
import os

SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if ' ' in auth_header:
                token = auth_header.split(" ")[1]
        
        if not token:
            return jsonify({'success': False, 'error': 'Token is missing!'}), 401
        
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
            if not current_user:
                 return jsonify({'success': False, 'error': 'User not found!'}), 401
        except Exception as e:
            return jsonify({'success': False, 'error': 'Token is invalid!', 'details': str(e)}), 401
            
        if args:
            return f(args[0], current_user, *args[1:], **kwargs)
        return f(current_user, *args, **kwargs)
    
    return decorated

# Routes
from .base import BaseAPI
from app.models.user import User
from app.database import db
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils import (
    validate_email, validate_password, validate_phone, 
    validate_name, validate_username, sanitize_string
)
from datetime import datetime, timedelta

# ... keep token_required ...
# It is defined above in the original file, so I don't need to re-type it if I use start/end lines carefully.
# Wait, I am replacing lines 54-58 (Routes section) and 7 (Import) primarily.
# But I need to add the Classes.

class SignupAPI(BaseAPI):
    """
    API for User Registration.
    Polymorphism: Overrides post() method.
    """
    def post(self):
        try:
            data = request.get_json()
            
            # Check required fields
            required_fields = ['email', 'username', 'password', 'full_name']
            missing_fields = [field for field in required_fields if field not in data or not data[field]]
            
            if missing_fields:
                return self.send_error(f'Missing required fields: {", ".join(missing_fields)}')
            
            # Sanitize inputs
            email = sanitize_string(data['email'].lower(), 254)
            username = sanitize_string(data['username'].lower(), 30)
            full_name = sanitize_string(data['full_name'], 50)
            password = data['password']
            phone = sanitize_string(data.get('phone', ''), 15)
            
            # Validation
            is_valid, error_msg = validate_email(email)
            if not is_valid: return self.send_error(error_msg)
            
            is_valid, error_msg = validate_username(username)
            if not is_valid: return self.send_error(error_msg)
            
            is_valid, error_msg = validate_password(password)
            if not is_valid: return self.send_error(error_msg)
            
            if phone:
                is_valid, error_msg = validate_phone(phone)
                if not is_valid: return self.send_error(error_msg)

            # Check existing (Direct DB usage, no repository layer)
            if User.query.filter_by(email=email).first():
                return self.send_error('Email already registered')
            
            if User.query.filter_by(username=username).first():
                return self.send_error('Username already taken')
            
            # Create user
            user = User(
                email=email,
                username=username,
                hashed_password=generate_password_hash(password),
                full_name=full_name,
                phone=phone if phone else None
            )
            
            db.session.add(user)
            db.session.commit()
            
            # Generate Token
            token = jwt.encode({
                'user_id': user.id,
                'exp': datetime.utcnow() + timedelta(days=7)
            }, SECRET_KEY, algorithm='HS256')
            
            return self.send_response({
                'message': 'User registered successfully',
                'token': token,
                'user': user.to_dict()
            }, status=201)
            
        except Exception as e:
            db.session.rollback()
            return self.send_error(str(e), 500)

class LoginAPI(BaseAPI):
    """
    API for User Login.
    Polymorphism: Overrides post() method.
    """
    def post(self):
        try:
            data = request.get_json()
            
            if not data.get('email') or not data.get('password'):
                return self.send_error('Email and password required')
            
            user = User.query.filter_by(email=data['email']).first()
            
            if not user or not check_password_hash(user.hashed_password, data['password']):
                return self.send_error('Invalid credentials', 401)
            
            token = jwt.encode({
                'user_id': user.id,
                'exp': datetime.utcnow() + timedelta(days=7)
            }, SECRET_KEY, algorithm='HS256')
            
            return self.send_response({
                'message': 'Login successful',
                'token': token,
                'user': user.to_dict()
            })
        except Exception as e:
            return self.send_error(str(e), 500)

# Register Class-Based Views
signup_view = SignupAPI.as_view('signup_api')
login_view = LoginAPI.as_view('login_api')

bp.add_url_rule('/signup', view_func=signup_view, methods=['POST'])
bp.add_url_rule('/login', view_func=login_view, methods=['POST'])
