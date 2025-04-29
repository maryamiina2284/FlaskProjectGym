# create_tables.py
from app import app, db, Member, Membership, User
with app.app_context():
    db.create_all()
    print("✅ Tables created successfully.")
