from app import app, db
from app.models.Model import User

with app.app_context():
    db.drop_all()
    db.create_all()