from api import app
from api import db

with app.app_context():
    db.create_all()