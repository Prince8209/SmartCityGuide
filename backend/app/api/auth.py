"""
Authentication API
User login and signup
"""
from flask import Blueprint, jsonify, request
from app.models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import os
from datetime import datetime, timedelta

bp = Blueprint('auth', __name__)
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')

from functools import wraps

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
            
        return f(current_user, *args, **kwargs)
    
    return decorated

@bp.route('/signup', methods=['POST'])
def signup():
    """Register new user"""
    try:
        data = request.get_json()
        
        if not all(k in data for k in ['email', 'username', 'password', 'full_name']):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'success': False, 'error': 'Email already registered'}), 400
        
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'success': False, 'error': 'Username already taken'}), 400
        
        user = User(
            email=data['email'],
            username=data['username'],
            hashed_password=generate_password_hash(data['password']),
            full_name=data['full_name']
        )
        
        db.session.add(user)
        db.session.commit()
        
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(days=7)
        }, SECRET_KEY, algorithm='HS256')
        
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'token': token,
            'user': user.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'success': False, 'error': 'Email and password required'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not check_password_hash(user.hashed_password, data['password']):
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
        
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(days=7)
        }, SECRET_KEY, algorithm='HS256')
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'token': token,
            'user': user.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
