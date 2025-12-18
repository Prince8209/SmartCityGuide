"""
Attraction Model
Represents tourist spots within a city
"""
from app.database.config import db
from sqlalchemy import String, Integer, Float, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Attraction(db.Model):
    __tablename__ = 'attractions'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey('cities.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(String(100), nullable=True)
    entry_fee: Mapped[int] = mapped_column(Integer, default=0)
    opening_hours: Mapped[str] = mapped_column(String(100), nullable=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)
    rating: Mapped[float] = mapped_column(Float, default=0.0)
    
    # Relationships
    city = relationship("City", back_populates="attractions")
    
    def to_dict(self):
        return {
            'id': self.id,
            'city_id': self.city_id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'entry_fee': self.entry_fee,
            'opening_hours': self.opening_hours,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'rating': self.rating
        }
    
    def __repr__(self):
        return f'<Attraction {self.name}>'
