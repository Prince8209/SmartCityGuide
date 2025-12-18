"""
Bookings API
Trip booking management
"""
from flask import Blueprint, jsonify, request
from app.models import Booking, db
from datetime import datetime
import random
import string

bookings_bp = Blueprint('bookings', __name__)

def generate_reference():
    """Generate unique booking reference"""
    return 'SCG' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

@bookings_bp.route('/api/bookings', methods=['POST'])
def create_booking():
    """Create new booking"""
    try:
        data = request.get_json()
        
        required = ['city_name', 'customer_name', 'customer_email', 'customer_phone',
                   'check_in_date', 'check_out_date', 'num_travelers', 'daily_budget']
        
        if not all(k in data for k in required):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        check_in = datetime.strptime(data['check_in_date'], '%Y-%m-%d').date()
        check_out = datetime.strptime(data['check_out_date'], '%Y-%m-%d').date()
        num_days = (check_out - check_in).days
        total_cost = num_days * data['daily_budget'] * data['num_travelers']
        
        booking = Booking(
            booking_reference=generate_reference(),
            city_name=data['city_name'],
            customer_name=data['customer_name'],
            customer_email=data['customer_email'],
            customer_phone=data['customer_phone'],
            check_in_date=check_in,
            check_out_date=check_out,
            num_travelers=data['num_travelers'],
            daily_budget=data['daily_budget'],
            total_cost=total_cost
        )
        
        db.session.add(booking)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Booking created successfully',
            'booking': booking.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@bookings_bp.route('/api/bookings', methods=['GET'])
def get_bookings():
    """Get all bookings"""
    try:
        bookings = Booking.query.order_by(Booking.created_at.desc()).all()
        return jsonify({
            'success': True,
            'count': len(bookings),
            'bookings': [b.to_dict() for b in bookings]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
