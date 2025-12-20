from app.main import create_app
from app.database.config import db
from app.models import Favorite

app = create_app()

with app.app_context():
    print("Creating database tables...")
    db.create_all()
    print("Tables created successfully.")
