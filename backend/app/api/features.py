"""
Features API
Consolidated endpoints for secondary features:
- Reviews
- Favorites
- Users (Navigation/Tracking)
- Upload
- Admin
"""
from flask import Blueprint, request, jsonify
from .base import BaseAPI
from app.database import db
from app.api.auth import token_required
from app.managers import user_tracker

# Models
from app.models.review import Review
from app.models.user import User
from app.models.favorite import Favorite
from app.models.city import City
from app.models.booking import Booking

# Utilities
import hmac
import hashlib
import uuid
import time
import os
from werkzeug.utils import secure_filename

# ==============================================================================
# 1. REVIEWS
# ==============================================================================
reviews_bp = Blueprint('reviews', __name__)

class ReviewListAPI(BaseAPI):
    @token_required
    def post(self, current_user):
        """Add a new review"""
        try:
            data = request.get_json()
            if not all(k in data for k in ['city_id', 'rating', 'comment']):
                return self.send_error('Missing required fields')
                
            existing_review = Review.query.filter_by(
                user_id=current_user.id, 
                city_id=data['city_id']
            ).first()
            
            if existing_review:
                return self.send_error('You have already reviewed this city')
                
            review = Review(
                user_id=current_user.id,
                city_id=data['city_id'],
                rating=data['rating'],
                comment=data['comment']
            )
            
            db.session.add(review)
            db.session.commit()
            
            return self.send_response({
                'message': 'Review added successfully',
                'review': review.to_dict()
            }, status=201)
        except Exception as e:
            db.session.rollback()
            return self.send_error(str(e), 500)

class CityReviewsAPI(BaseAPI):
    def get(self, city_id):
        """Get reviews for a city"""
        try:
            reviews = Review.query.filter_by(city_id=city_id).order_by(Review.created_at.desc()).all()
            reviews_data = []
            for review in reviews:
                user = User.query.get(review.user_id)
                review_dict = review.to_dict()
                review_dict['user_name'] = user.full_name if user else 'Anonymous'
                reviews_data.append(review_dict)
            return self.send_response({
                'count': len(reviews_data),
                'reviews': reviews_data
            })
        except Exception as e:
            return self.send_error(str(e), 500)

reviews_bp.add_url_rule('', view_func=ReviewListAPI.as_view('review_create'), methods=['POST'])
reviews_bp.add_url_rule('/<int:city_id>', view_func=CityReviewsAPI.as_view('city_reviews'), methods=['GET'])


# ==============================================================================
# 2. FAVORITES
# ==============================================================================
favorites_bp = Blueprint('favorites', __name__)

class FavoriteListAPI(BaseAPI):
    @token_required
    def get(self, current_user):
        try:
            favorites = Favorite.query.filter_by(user_id=current_user.id).all()
            favorite_ids = [f.city_id for f in favorites]
            return self.send_response({'favorites': favorite_ids})
        except Exception as e:
            return self.send_error(str(e), 500)

class FavoriteDetailAPI(BaseAPI):
    @token_required
    def post(self, current_user, city_id):
        try:
            existing = Favorite.query.filter_by(user_id=current_user.id, city_id=city_id).first()
            if existing: return self.send_response({'message': 'Already in favorites'})
            
            favorite = Favorite(user_id=current_user.id, city_id=city_id)
            db.session.add(favorite)
            db.session.commit()
            return self.send_response({'message': 'Added to favorites'}, status=201)
        except Exception as e:
            db.session.rollback()
            return self.send_error(str(e), 500)

    @token_required
    def delete(self, current_user, city_id):
        try:
            favorite = Favorite.query.filter_by(user_id=current_user.id, city_id=city_id).first()
            if not favorite: return self.send_error('Favorite not found', 404)
            
            db.session.delete(favorite)
            db.session.commit()
            return self.send_response({'message': 'Removed from favorites'})
        except Exception as e:
            db.session.rollback()
            return self.send_error(str(e), 500)

favorites_bp.add_url_rule('', view_func=FavoriteListAPI.as_view('favorite_list'), methods=['GET'])
favorites_bp.add_url_rule('/<int:city_id>', view_func=FavoriteDetailAPI.as_view('favorite_detail'), methods=['POST', 'DELETE'])


# ==============================================================================
# 3. USERS (Navigation)
# ==============================================================================
users_bp = Blueprint('users', __name__)

class UserTrackAPI(BaseAPI):
    def post(self):
        try:
            data = request.get_json()
            if not data.get('user_id') or not data.get('page'):
                return self.send_error('user_id and page required')
            user_tracker.track_navigation(data['user_id'], data['page'])
            return self.send_response({'message': 'Navigation tracked successfully'})
        except Exception as e:
            return self.send_error(str(e), 500)

class UserHistoryAPI(BaseAPI):
    def get(self):
        try:
            user_id = request.args.get('user_id')
            limit = request.args.get('limit', 10, type=int)
            if not user_id: return self.send_error('user_id required')
            history = user_tracker.get_navigation_history(user_id, limit)
            return self.send_response({'count': len(history), 'history': history})
        except Exception as e:
            return self.send_error(str(e), 500)

class UserBackAPI(BaseAPI):
    def post(self):
        try:
            data = request.get_json()
            if not data.get('user_id'): return self.send_error('user_id required')
            previous_page = user_tracker.go_back(data['user_id'])
            if previous_page:
                return self.send_response({'previous_page': previous_page})
            else:
                return self.send_error('No previous page in history', 404)
        except Exception as e:
            return self.send_error(str(e), 500)

class UserRecentCitiesAPI(BaseAPI):
    def get(self):
        try:
            user_id = request.args.get('user_id')
            if not user_id: return self.send_error('user_id required')
            recent_cities = user_tracker.get_recent_cities(user_id)
            return self.send_response({'count': len(recent_cities), 'recent_cities': recent_cities})
        except Exception as e:
            return self.send_error(str(e), 500)

users_bp.add_url_rule('/navigation', view_func=UserTrackAPI.as_view('user_track'))
users_bp.add_url_rule('/navigation/history', view_func=UserHistoryAPI.as_view('user_history'))
users_bp.add_url_rule('/navigation/back', view_func=UserBackAPI.as_view('user_back'))
users_bp.add_url_rule('/recent-cities', view_func=UserRecentCitiesAPI.as_view('recent_cities'))


# ==============================================================================
# 4. UPLOAD
# ==============================================================================
upload_bp = Blueprint('upload', __name__)

class UploadConfigAPI(BaseAPI):
    def get(self):
        return self.send_response({
            "publicKey": os.getenv('IMAGEKIT_PUBLIC_KEY'),
            "urlEndpoint": os.getenv('IMAGEKIT_URL_ENDPOINT')
        })

class UploadAuthAPI(BaseAPI):
    def get(self):
        try:
            private_key = os.getenv('IMAGEKIT_PRIVATE_KEY', '')
            token = str(uuid.uuid4())
            expire = str(int(time.time()) + 1800)
            data = f"{token}{expire}"
            signature = hmac.new(private_key.encode(), data.encode(), hashlib.sha1).hexdigest()
            return jsonify({ "token": token, "expire": expire, "signature": signature })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

class UploadLocalAPI(BaseAPI):
    def post(self):
        try:
            if 'file' not in request.files: return self.send_error('No file part')
            file = request.files['file']
            if file.filename == '': return self.send_error('No selected file')
            if file:
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4().hex[:8]}_{filename}"
                base_dir = os.getcwd() 
                assets_dir = os.path.join(base_dir, 'frontend', 'assets', 'images', 'cities')
                if not os.path.exists(assets_dir): os.makedirs(assets_dir)
                file.save(os.path.join(assets_dir, unique_filename))
                return self.send_response({'filename': unique_filename, 'url': unique_filename})
        except Exception as e:
            return self.send_error(str(e), 500)

upload_bp.add_url_rule('/config', view_func=UploadConfigAPI.as_view('upload_config'))
upload_bp.add_url_rule('/auth', view_func=UploadAuthAPI.as_view('upload_auth'))
upload_bp.add_url_rule('/local', view_func=UploadLocalAPI.as_view('upload_local'))


# ==============================================================================
# 5. ADMIN
# ==============================================================================
admin_bp = Blueprint('admin', __name__)

class AdminStatsAPI(BaseAPI):
    @token_required
    def get(self, current_user):
        if not current_user.is_admin: return self.send_error('Admin privileges required', 403)
        try:
            stats = {
                'cities': City.query.count(),
                'users': User.query.count(),
                'bookings': Booking.query.count(),
                'reviews': Review.query.count()
            }
            return self.send_response({'stats': stats})
        except Exception as e:
            return self.send_error(str(e), 500)

class AdminUsersAPI(BaseAPI):
    @token_required
    def get(self, current_user):
        if not current_user.is_admin: return self.send_error('Admin privileges required', 403)
        try:
            users = User.query.all()
            return self.send_response({'users': [user.to_dict() for user in users]})
        except Exception as e:
            return self.send_error(str(e), 500)

admin_bp.add_url_rule('/stats', view_func=AdminStatsAPI.as_view('admin_stats'), methods=['GET'])
admin_bp.add_url_rule('/users', view_func=AdminUsersAPI.as_view('admin_users'), methods=['GET'])
