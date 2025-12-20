from app.main import create_app
from app.database.config import db
from sqlalchemy import inspect

app = create_app()

with app.app_context():
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"Tables in database: {tables}")
    
    if 'favorites' in tables:
        columns = [c['name'] for c in inspector.get_columns('favorites')]
        print(f"Favorites columns: {columns}")
    else:
        print("ERROR: 'favorites' table NOT found!")
