from app import db, app, models

with app.app_context():
    db.create_all()