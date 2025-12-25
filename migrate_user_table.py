import sys
import os
from sqlalchemy import text

sys.path.append(os.path.join(os.getcwd(), 'backend'))
from app.main import create_app
from app.database.config import db

def migrate():
    print("🔄 Starting User Table Migration...")
    app = create_app()
    
    with app.app_context():
        try:
            print("   - Attempting to add 'phone' column...")
            with db.engine.connect() as conn:
                conn.execute(text("ALTER TABLE users ADD COLUMN phone VARCHAR(20) NULL;"))
                conn.commit()
            print("✅ Migration Successful: 'phone' column added.")
        except Exception as e:
            if "Duplicate column name" in str(e):
                print("ℹ️ Column 'phone' already exists.")
            else:
                print(f"❌ Migration Failed: {e}")

if __name__ == '__main__':
    migrate()
