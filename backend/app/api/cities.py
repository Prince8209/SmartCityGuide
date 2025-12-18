"""
Cities API
Endpoints for fetching cities from database
"""
from flask import Blueprint, jsonify, request
from app.models import City, Attraction, db
from sqlalchemy import or_
from app.api.auth import token_required

bp = Blueprint('cities', __name__)

@bp.route('', methods=['GET'])
def get_cities():
    """Get all cities with optional filtering"""
    try:
        query = City.query
        
        # Search filter
        search = request.args.get('search', '').strip()
        if search:
            pattern = f'%{search}%'
            query = query.filter(or_(
                City.name.ilike(pattern),
                City.state.ilike(pattern),
                City.description.ilike(pattern)
            ))
        
        # Region filter
        region = request.args.get('region', '').strip()
        if region:
            query = query.filter(City.region == region)
        
        # Trip type filter
        trip_type = request.args.get('trip_type', '').strip()
        if trip_type:
            query = query.filter(City.trip_types.contains([trip_type]))
        
        # Budget filter
        budget_max = request.args.get('budget_max', type=int)
        if budget_max:
            query = query.filter(City.avg_budget_per_day <= budget_max)
        
        # Pagination
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 9, type=int)
        
        pagination = query.paginate(page=page, per_page=limit, error_out=False)
        cities = pagination.items
        
        return jsonify({
            'success': True,
            'count': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'has_next': pagination.has_next,
            'cities': [city.to_dict() for city in cities]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/<int:city_id>', methods=['GET'])
def get_city(city_id):
    """Get single city by ID"""
    try:
        city = City.query.get_or_404(city_id)
        return jsonify({'success': True, 'city': city.to_dict_details()})
    except:
        return jsonify({'success': False, 'error': 'City not found'}), 404

@bp.route('/regions', methods=['GET'])
def get_regions():
    """Get all unique regions"""
    try:
        regions = db.session.query(City.region).distinct().filter(City.region.isnot(None)).all()
        return jsonify({
            'success': True,
            'regions': sorted([r[0] for r in regions if r[0]])
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/trip-types', methods=['GET'])
def get_trip_types():
    """Get all unique trip types"""
    try:
        cities = City.query.filter(City.trip_types.isnot(None)).all()
        trip_types = set()
        for city in cities:
            if city.trip_types:
                trip_types.update(city.trip_types)
        
        return jsonify({
            'success': True,
            'trip_types': sorted(list(trip_types))
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/attraction-categories', methods=['GET'])
def get_attraction_categories():
    """Get all unique attraction categories"""
    try:
        from app.models import Attraction
        categories = db.session.query(Attraction.category).distinct().filter(Attraction.category.isnot(None)).all()
        return jsonify({
            'success': True,
            'categories': sorted([c[0] for c in categories if c[0]])
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('', methods=['POST'])
@token_required
def create_city(current_user):
    """Create a new city (Admin only)"""
    try:
        if not current_user.is_admin:
            return jsonify({'success': False, 'error': 'Admin privileges required'}), 403

        data = request.get_json()
        
        # Validation
        if not all(k in data for k in ['name', 'state', 'description']):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400

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

        # Add Attractions
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

        return jsonify({
            'success': True,
            'message': 'City created successfully',
            'city': city.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
