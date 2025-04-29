from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(200))
    role = db.Column(db.String(50))
    status = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)



class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))
    membership_id = db.Column(db.Integer, db.ForeignKey('membership.id'))

class Membership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    membership_type = db.Column(db.String(100))
    duration = db.Column(db.Integer)


class Charge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))
    user_id = db.Column(db.Integer)
    price = db.Column(db.Float)
    remarks = db.Column(db.String(255))
    date = db.Column(db.DateTime, default=datetime.utcnow)

class Trainer(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class ClassSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(100))
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
