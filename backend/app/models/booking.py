"""
Booking Model
Trip bookings
"""
from datetime import datetime
from app.database.config import db
from sqlalchemy import String, Integer, Text, DateTime, Date
from sqlalchemy.orm import Mapped, mapped_column

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    booking_reference: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    city_name: Mapped[str] = mapped_column(String(255), nullable=False)
    customer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    customer_email: Mapped[str] = mapped_column(String(255), nullable=False)
    customer_phone: Mapped[str] = mapped_column(String(20), nullable=False)
    check_in_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    check_out_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    num_travelers: Mapped[int] = mapped_column(Integer, nullable=False)
    daily_budget: Mapped[int] = mapped_column(Integer, nullable=False)
    total_cost: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default='confirmed')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'booking_reference': self.booking_reference,
            'city_name': self.city_name,
            'customer_name': self.customer_name,
            'customer_email': self.customer_email,
            'customer_phone': self.customer_phone,
            'check_in_date': self.check_in_date.isoformat() if self.check_in_date else None,
            'check_out_date': self.check_out_date.isoformat() if self.check_out_date else None,
            'num_travelers': self.num_travelers,
            'daily_budget': self.daily_budget,
            'total_cost': self.total_cost,
            'status': self.status
        }
    
    def __repr__(self):
        return f'<Booking {self.booking_reference}>'
