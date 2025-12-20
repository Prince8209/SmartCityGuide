"""
Admin API
Dashboard statistics and management endpoints
"""
from flask import Blueprint, jsonify
from app.models import City, User, Booking, Review, db
from app.api.auth import token_required

bp = Blueprint('admin', __name__)

@bp.route('/stats', methods=['GET'])
@token_required
def get_stats(current_user):
    """Get dashboard statistics"""
    if not current_user.is_admin:
        return jsonify({'success': False, 'error': 'Admin privileges required'}), 403
        
    try:
        stats = {
            'cities': City.query.count(),
            'users': User.query.count(),
            'bookings': Booking.query.count(),
            'reviews': Review.query.count()
        }
        return jsonify({'success': True, 'stats': stats})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/users', methods=['GET'])
@token_required
def get_users(current_user):
    """Get all users"""
    if not current_user.is_admin:
        return jsonify({'success': False, 'error': 'Admin privileges required'}), 403
        
    try:
        users = User.query.all()
        return jsonify({
            'success': True,
            'users': [user.to_dict() for user in users]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
