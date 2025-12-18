"""
Reviews API
Manage city reviews and ratings
"""
from flask import Blueprint, jsonify, request
from app.models import Review, User, db
from app.api.auth import token_required

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/<int:city_id>', methods=['GET'])
def get_reviews(city_id):
    """Get all reviews for a city"""
    try:
        reviews = Review.query.filter_by(city_id=city_id).order_by(Review.created_at.desc()).all()
        
        # Enrich with user data
        reviews_data = []
        for review in reviews:
            user = User.query.get(review.user_id)
            review_dict = review.to_dict()
            review_dict['user_name'] = user.full_name if user else 'Anonymous'
            reviews_data.append(review_dict)
            
        return jsonify({
            'success': True,
            'count': len(reviews_data),
            'reviews': reviews_data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@reviews_bp.route('/', methods=['POST'])
@token_required
def add_review(current_user):
    """Add a new review"""
    try:
        data = request.get_json()
        
        if not all(k in data for k in ['city_id', 'rating', 'comment']):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
            
        # Check if user already reviewed this city
        existing_review = Review.query.filter_by(
            user_id=current_user.id, 
            city_id=data['city_id']
        ).first()
        
        if existing_review:
            return jsonify({'success': False, 'error': 'You have already reviewed this city'}), 400
            
        review = Review(
            user_id=current_user.id,
            city_id=data['city_id'],
            rating=data['rating'],
            comment=data['comment']
        )
        
        db.session.add(review)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Review added successfully',
            'review': review.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
