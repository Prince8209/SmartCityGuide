"""
Database Seeding Script
Creates tables and loads sample data
"""
import pymysql
import sys
sys.path.insert(0, '.')

from app.main import create_app
from app.database import db

app = create_app()

with app.app_context():
    print("Dropping existing tables...")
    try:
        db.session.execute(db.text('SET FOREIGN_KEY_CHECKS = 0'))
        db.session.execute(db.text('DROP TABLE IF EXISTS favorites'))
        db.session.execute(db.text('DROP TABLE IF EXISTS reviews'))
        db.session.execute(db.text('DROP TABLE IF EXISTS bookings'))
        db.session.execute(db.text('DROP TABLE IF EXISTS attractions'))
        db.session.execute(db.text('DROP TABLE IF EXISTS cities'))
        db.session.execute(db.text('DROP TABLE IF EXISTS users'))
        db.session.execute(db.text('SET FOREIGN_KEY_CHECKS = 1'))
        db.session.commit()
    except Exception as e:
        print(f"Error dropping tables: {e}")
        db.session.rollback()

    print("Creating database tables...")
    db.create_all()
    print("✓ Tables created")
    
    # Load sample data from SQL file
    print("Loading sample data...")
    with open('sample_data.sql', 'r', encoding='utf-8') as f:
        sql = f.read()
    
    # Remove comments and split statements
    lines = [l for l in sql.splitlines() if not l.strip().startswith('--')]
    clean_sql = '\n'.join(lines)
    statements = [s.strip() for s in clean_sql.split(';') if s.strip()]
    
    for stmt in statements:
        if stmt and 'INSERT' in stmt.upper():
            try:
                # print(f"Executing: {stmt[:50]}...")
                db.session.execute(db.text(stmt))
            except Exception as e:
                print(f"Warning: {e}")
                print(f"Statement: {stmt[:100]}...")
    
    db.session.commit()
    print("✓ Database seeded successfully")
    print("\nDatabase setup complete!")
