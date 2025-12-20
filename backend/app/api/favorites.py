"""
Favorites API
Manage user favorite cities
"""
from flask import Blueprint, jsonify
from app.models import Favorite, db
from app.api.auth import token_required

bp = Blueprint('favorites', __name__)

@bp.route('', methods=['GET'])
@token_required
def get_favorites(current_user):
    """Get all favorite cities for the current user"""
    try:
        favorites = Favorite.query.filter_by(user_id=current_user.id).all()
        # Return list of city IDs for easy frontend checking
        favorite_ids = [f.city_id for f in favorites]
        return jsonify({
            'success': True,
            'favorites': favorite_ids
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/<int:city_id>', methods=['POST'])
@token_required
def add_favorite(current_user, city_id):
    """Add a city to favorites"""
    try:
        # Check if already favorited
        existing = Favorite.query.filter_by(
            user_id=current_user.id,
            city_id=city_id
        ).first()
        
        if existing:
            return jsonify({'success': True, 'message': 'Already in favorites'}), 200
            
        favorite = Favorite(
            user_id=current_user.id,
            city_id=city_id
        )
        
        db.session.add(favorite)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Added to favorites'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/<int:city_id>', methods=['DELETE'])
@token_required
def remove_favorite(current_user, city_id):
    """Remove a city from favorites"""
    try:
        favorite = Favorite.query.filter_by(
            user_id=current_user.id,
            city_id=city_id
        ).first()
        
        if not favorite:
            return jsonify({'success': False, 'error': 'Favorite not found'}), 404
            
        db.session.delete(favorite)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Removed from favorites'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
