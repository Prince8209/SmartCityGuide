"""
Bookings API
Trip booking management
Refactored to use OOP Class-Based Views
"""
from flask import Blueprint, request
from .base import BaseAPI
from app.models.booking import Booking
from app.database import db
from app.api.auth import token_required
from app.managers import booking_queue_manager
from datetime import datetime
import random
import string

bookings_bp = Blueprint('bookings', __name__)

class BookingListAPI(BaseAPI):
    """
    API for Booking operations
    """
    def _generate_reference(self):
        """Generate unique booking reference (Encapsulated helper)"""
        return 'SCG' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    @token_required
    def get(self, current_user):
        """Get bookings"""
        try:
            if current_user.is_admin:
                bookings = Booking.query.order_by(Booking.created_at.desc()).all()
            else:
                bookings = Booking.query.filter_by(customer_email=current_user.email).order_by(Booking.created_at.desc()).all()

            return self.send_response({
                'count': len(bookings),
                'bookings': [b.to_dict() for b in bookings]
            })
        except Exception as e:
            return self.send_error(str(e), 500)

    # Note: create (POST) was originally public in controller logic (no token_required), 
    # but usually bookings require auth or at least user info. 
    # The controller code extracted email from request data, implying public or manual entry.
    # I will keep it as per controller (no @token_required on post), but ideally it should be specific.
    def post(self):
        """Create new booking"""
        try:
            data = request.get_json()
            
            required = ['city_name', 'customer_name', 'customer_email', 'customer_phone',
                       'check_in_date', 'check_out_date', 'num_travelers', 'daily_budget']
            
            if not all(k in data for k in required):
                return self.send_error('Missing required fields')
            
            check_in = datetime.strptime(data['check_in_date'], '%Y-%m-%d').date()
            check_out = datetime.strptime(data['check_out_date'], '%Y-%m-%d').date()
            num_days = (check_out - check_in).days
            total_cost = num_days * data['daily_budget'] * data['num_travelers']
            
            booking_data = {
                'booking_reference': self._generate_reference(),
                'city_name': data['city_name'],
                'customer_name': data['customer_name'],
                'customer_email': data['customer_email'],
                'customer_phone': data['customer_phone'],
                'check_in_date': str(check_in),
                'check_out_date': str(check_out),
                'num_travelers': data['num_travelers'],
                'daily_budget': data['daily_budget'],
                'total_cost': total_cost
            }
            
            # Add to queue
            queue_status = booking_queue_manager.enqueue_booking(booking_data)
            
            # Save to DB
            booking = Booking(
                booking_reference=booking_data['booking_reference'],
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
            
            return self.send_response({
                'message': 'Booking created and queued for processing',
                'booking': booking.to_dict(),
                'queue_info': queue_status
            }, status=201)
        except Exception as e:
            db.session.rollback()
            return self.send_error(str(e), 500)

class QueueStatusAPI(BaseAPI):
    def get(self):
        try:
            status = booking_queue_manager.get_queue_status()
            return self.send_response({'queue_status': status})
        except Exception as e:
            return self.send_error(str(e), 500)

# Register Routes
booking_view = BookingListAPI.as_view('booking_list')
queue_view = QueueStatusAPI.as_view('queue_status')

bookings_bp.add_url_rule('/api/bookings', view_func=booking_view, methods=['POST', 'GET'])
bookings_bp.add_url_rule('/api/bookings/queue/status', view_func=queue_view, methods=['GET'])
