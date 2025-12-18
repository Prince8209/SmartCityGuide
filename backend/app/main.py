"""
Smart City Guide - Flask Application
Main entry point
"""



import pymysql
pymysql.install_as_MySQLdb()

import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from app.database import db, init_db

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://root:@localhost:3306/smart_city_guide'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSON_SORT_KEYS'] = False
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Initialize database
    init_db(app)
    
    # Register blueprints
    from app.api import auth, cities, bookings, reviews
    
    app.register_blueprint(auth.bp, url_prefix='/api/auth')
    app.register_blueprint(cities.bp, url_prefix='/api/cities')
    app.register_blueprint(bookings.bookings_bp)
    app.register_blueprint(reviews.reviews_bp, url_prefix='/api/reviews')
    
    from app.api.upload import upload_bp
    app.register_blueprint(upload_bp, url_prefix='/api/upload')
    
    # Root endpoint
    @app.route('/')
    def index():
        return jsonify({
            'name': 'Smart City Guide API',
            'version': '2.0.0',
            'database': 'MySQL',
            'endpoints': {
                'cities': '/api/cities',
                'auth': '/api/auth',
                'bookings': '/api/bookings'
            }
        })
    
    # Health check
    @app.route('/api/health')
    def health():
        try:
            db.session.execute(db.text('SELECT 1'))
            return jsonify({'status': 'healthy', 'database': 'connected'})
        except:
            return jsonify({'status': 'unhealthy', 'database': 'disconnected'}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("=" * 60)
    print("🚀 Smart City Guide Backend")
    print("=" * 60)
    print("📍 API: http://localhost:5000")
    print("📊 Database: MySQL")
    print("💡 Admin: admin@smartcityguide.com / admin123")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
