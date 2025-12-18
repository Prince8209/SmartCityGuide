"""
City Model
Represents travel destinations
"""
from datetime import datetime
from app.database.config import db
from sqlalchemy import String, Integer, Float, Text, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

class City(db.Model):
    __tablename__ = 'cities'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    state: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    image_url: Mapped[str] = mapped_column(String(500), nullable=True)
    badge: Mapped[str] = mapped_column(String(100), nullable=True)
    best_season: Mapped[str] = mapped_column(String(100), nullable=True)
    avg_budget_per_day: Mapped[int] = mapped_column(Integer, nullable=True)
    recommended_days: Mapped[str] = mapped_column(String(50), nullable=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)
    category: Mapped[str] = mapped_column(String(100), nullable=True)
    region: Mapped[str] = mapped_column(String(50), nullable=True)
    trip_types: Mapped[list] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    attractions = relationship("Attraction", back_populates="city", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'state': self.state,
            'description': self.description,
            'image_url': self.image_url,
            'badge': self.badge,
            'best_season': self.best_season,
            'avg_budget_per_day': self.avg_budget_per_day,
            'recommended_days': self.recommended_days,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'category': self.category,
            'region': self.region,
            'trip_types': self.trip_types
        }

    def to_dict_details(self):
        data = self.to_dict()
        data['attractions'] = [a.to_dict() for a in self.attractions]
        return data
    
    def __repr__(self):
        return f'<City {self.name}>'
