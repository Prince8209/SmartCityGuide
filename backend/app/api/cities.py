"""
Cities API
Endpoints for fetching cities from database
Refactored to use OOP Class-Based Views
"""
from flask import Blueprint, request, current_app
from .base import BaseAPI
from app.models.city import City
from app.models.attraction import Attraction
from app.database import db
from app.api.auth import token_required
from sqlalchemy import or_, String
from app.managers import city_cache
from app.managers import rating_manager
from app.managers import user_tracker

bp = Blueprint('cities', __name__)

class CityListAPI(BaseAPI):
    """
    API for City Listing and Creation.
    Inheritance: Inherits from BaseAPI.
    """
    def get(self):
        """Get all cities with filtered query"""
        try:
            # Extract query params
            search = request.args.get('search', '').strip()
            region = request.args.get('region', '').strip()
            trip_type = request.args.get('trip_type', '').strip()
            budget_max = request.args.get('budget_max', type=int)
            page = request.args.get('page', 1, type=int)
            limit = request.args.get('limit', 9, type=int)
            
            # Query Construction
            query = City.query
            
            if search:
                pattern = f'%{search}%'
                query = query.filter(or_(
                    City.name.ilike(pattern),
                    City.state.ilike(pattern),
                    City.description.ilike(pattern)
                ))
            
            if region:
                query = query.filter(City.region == region)
                
            if trip_type:
                # Use string matching for broad compatibility (SQLite JSON is text)
                query = query.filter(City.trip_types.cast(String).ilike(f'%"{trip_type}"%'))
                
            if budget_max:
                query = query.filter(City.avg_budget_per_day <= budget_max)
                
            pagination = query.paginate(page=page, per_page=limit, error_out=False)
            cities = pagination.items
            
            return self.send_response({
                'count': pagination.total,
                'pages': pagination.pages,
                'current_page': page,
                'has_next': pagination.has_next,
                'cities': [city.to_dict() for city in cities]
            })
        except Exception as e:
            return self.send_error(str(e), 500)

    @token_required
    def post(self, current_user):
        """Create a new city (Admin only)"""
        try:
            if not current_user.is_admin:
                return self.send_error('Admin privileges required', 403)

            data = request.get_json()
            
            if not all(k in data for k in ['name', 'state', 'description']):
                return self.send_error('Missing required fields')

            city = City(
                name=data['name'],
                state=data['state'],
                description=data['description'],
                image_url=data.get('image_url'),
                category=data.get('category'),
                region=data.get('region'),
                avg_budget_per_day=float(data.get('avg_budget_per_day', 0) or 0),
                trip_types=data.get('trip_types', []),
                best_season=data.get('best_season'),
                recommended_days=data.get('recommended_days')
            )
            
            db.session.add(city)
            db.session.flush() # Get ID
            
            if 'attractions' in data and isinstance(data['attractions'], list):
                for attr_data in data['attractions']:
                    attraction = Attraction(
                        city_id=city.id,
                        name=attr_data.get('name'),
                        category=attr_data.get('category'),
                        description=attr_data.get('description')
                    )
                    db.session.add(attraction)
            
            db.session.commit()

            return self.send_response({
                'message': 'City created successfully',
                'city': city.to_dict()
            }, status=201)

        except Exception as e:
            db.session.rollback()
            return self.send_error(str(e), 500)

class CityDetailAPI(BaseAPI):
    """
    API for Single City Operations.
    """
    def get(self, city_id):
        try:
            # Check cache
            cache_key = f'city_{city_id}'
            cached_city = city_cache.get(cache_key)
            
            if cached_city:
                # Track recent city view
                user_id = request.args.get('user_id')
                if user_id:
                    user_tracker.add_recent_city(user_id, city_id, cached_city.get('name', ''))
                return self.send_response({'city': cached_city, 'from_cache': True})
            
            # Fetch from DB
            city = City.query.get_or_404(city_id)
            city_data = city.to_dict_details()
            
            # Cache result
            city_cache.set(cache_key, city_data)
            
            # Track
            user_id = request.args.get('user_id')
            if user_id:
                user_tracker.add_recent_city(user_id, city_id, city.name)
            
            # Add rating to BST
            if hasattr(city, 'rating') and city.rating:
                rating_manager.add_rating(city_id, int(city.rating))
            
            return self.send_response({'city': city_data, 'from_cache': False})
        except Exception as e:
             if '404' in str(e): return self.send_error('City not found', 404)
             return self.send_error(str(e), 500)

    @token_required
    def put(self, current_user, city_id):
        try:
            if not current_user.is_admin:
                return self.send_error('Admin privileges required', 403)

            city = City.query.get_or_404(city_id)
            data = request.get_json()

            fields = ['name', 'state', 'description', 'image_url', 'category', 
                      'region', 'best_season', 'recommended_days', 'trip_types']
            
            for field in fields:
                if field in data:
                    setattr(city, field, data[field])
            
            if 'avg_budget_per_day' in data:
                 city.avg_budget_per_day = float(data.get('avg_budget_per_day') or 0)
            
            db.session.commit()
            
            # Invalidate cache
            city_cache.delete(f'city_{city_id}')

            return self.send_response({
                'message': 'City updated successfully',
                'city': city.to_dict()
            })
        except Exception as e:
            db.session.rollback()
            return self.send_error(str(e), 500)

    @token_required
    def delete(self, current_user, city_id):
        try:
            if not current_user.is_admin:
                return self.send_error('Admin privileges required', 403)

            city = City.query.get_or_404(city_id)
            db.session.delete(city)
            db.session.commit()
            
            city_cache.delete(f'city_{city_id}')

            return self.send_response({'message': 'City deleted successfully'})
        except Exception as e:
            db.session.rollback()
            return self.send_error(str(e), 500)

class RegionAPI(BaseAPI):
    def get(self):
        try:
            regions = db.session.query(City.region).distinct().filter(City.region.isnot(None)).all()
            return self.send_response({'regions': sorted([r[0] for r in regions if r[0]])})
        except Exception as e:
            return self.send_error(str(e), 500)

class TripTypeAPI(BaseAPI):
    def get(self):
        try:
            cities = City.query.filter(City.trip_types.isnot(None)).all()
            trip_types = set()
            for city in cities:
                if city.trip_types:
                    trip_types.update(city.trip_types)
            return self.send_response({'trip_types': sorted(list(trip_types))})
        except Exception as e:
            return self.send_error(str(e), 500)

class AttractionCategoryAPI(BaseAPI):
    def get(self):
        try:
            categories = db.session.query(Attraction.category).distinct().filter(Attraction.category.isnot(None)).all()
            return self.send_response({'categories': sorted([c[0] for c in categories if c[0]])})
        except Exception as e:
            return self.send_error(str(e), 500)

class TopRatedCityAPI(BaseAPI):
    def get(self):
        try:
            limit = request.args.get('limit', 10, type=int)
            top_ratings = rating_manager.get_top_ratings(limit)
            
            cities_data = []
            for item in top_ratings:
                city = City.query.get(item['city_id'])
                if city:
                    city_dict = city.to_dict()
                    city_dict['rating'] = item['rating']
                    cities_data.append(city_dict)
            
            return self.send_response({
                'count': len(cities_data),
                'cities': cities_data
            })
        except Exception as e:
            return self.send_error(str(e), 500)

class RatingStatsAPI(BaseAPI):
    def get(self):
        try:
            stats = rating_manager.get_rating_stats()
            return self.send_response({'stats': stats})
        except Exception as e:
            return self.send_error(str(e), 500)

class CacheStatsAPI(BaseAPI):
    def get(self):
        try:
            stats = city_cache.get_stats()
            return self.send_response({'cache_stats': stats})
        except Exception as e:
            return self.send_error(str(e), 500)

class ExploreCityAPI(BaseAPI):
    """
    API to explore a random city.
    """
    def get(self):
        try:
            # Fetch all city IDs efficiently
            cities = db.session.query(City.id).all()
            if not cities:
                return self.send_error('No cities found', 404)
            
            # Select random city
            import random
            random_id = random.choice([c[0] for c in cities])
            return self.send_response({'city_id': random_id})
        except Exception as e:
             return self.send_error(str(e), 500)

# Register Class-Based Views
city_view = CityListAPI.as_view('city_list')
bp.add_url_rule('', view_func=city_view, methods=['GET', 'POST'])

city_detail_view = CityDetailAPI.as_view('city_detail')
bp.add_url_rule('/<int:city_id>', view_func=city_detail_view, methods=['GET', 'PUT', 'DELETE'])

# Metadata Routes
bp.add_url_rule('/regions', view_func=RegionAPI.as_view('regions'))
bp.add_url_rule('/trip-types', view_func=TripTypeAPI.as_view('trip_types'))
bp.add_url_rule('/attraction-categories', view_func=AttractionCategoryAPI.as_view('attraction_categories'))

# Stats and Special Routes
bp.add_url_rule('/top-rated', view_func=TopRatedCityAPI.as_view('top_rated'))
bp.add_url_rule('/ratings/stats', view_func=RatingStatsAPI.as_view('rating_stats'))
bp.add_url_rule('/cache/stats', view_func=CacheStatsAPI.as_view('cache_stats'))
bp.add_url_rule('/explore', view_func=ExploreCityAPI.as_view('explore_city'))
