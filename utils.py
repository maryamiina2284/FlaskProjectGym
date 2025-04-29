from models import db, Member, Membership, Charge, Trainer, Equipment, ClassSchedule
from flask import session
from datetime import datetime
from sqlalchemy import func

def read_all(model):
    return model.query.all()

def read_where(model, **kwargs):
    return model.query.filter_by(**kwargs).all()

def read_column(model, column, id_):
    obj = model.query.get(id_)
    return getattr(obj, column, None) if obj else None

def insert(model, data):
    obj = model(**data)
    db.session.add(obj)
    db.session.commit()
    return True

def update(model, id_, data):
    obj = model.query.get(id_)
    if obj:
        for k, v in data.items():
            setattr(obj, k, v)
        db.session.commit()
        return True
    return False

def delete(model, id_):
    obj = model.query.get(id_)
    if obj:
        db.session.delete(obj)
        db.session.commit()
        return True
    return False

def charge_all_members():
    for member in Member.query.all():
        charge_member(member.id)

def charge_member(member_id):
    membership_id = read_column(Member, 'membership_id', member_id)
    price = read_column(Membership, 'price', membership_id)
    
    current_month = datetime.utcnow().strftime('%Y-%m')
    already_charged = Charge.query.filter(
        Charge.member_id == member_id,
        func.date_format(Charge.date, '%Y-%m') == current_month
    ).count()

    if already_charged:
        return False

    charge = Charge(
        member_id=member_id,
        user_id=session.get('user_id'),
        price=price,
        remarks=f"{datetime.utcnow().strftime('%B, %Y')} Charge"
    )
    db.session.add(charge)
    db.session.commit()
    return True

def get_class_schedule(class_name):
    return ClassSchedule.query.filter_by(class_name=class_name).all()

def get_count(model):
    return db.session.query(model).count()

def get_sum(model, column):
    return db.session.query(func.sum(getattr(model, column))).scalar() or 0

def check_if_charged():
    pattern = datetime.utcnow().strftime('%Y-%m')
    charges = Charge.query.filter(func.date_format(Charge.date, '%Y-%m') == pattern).all()
    return len(charges) > 0
