from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from models import db, Member, Membership, Charge, User, Equipment, ClassSchedule, Trainer

from utils import charge_all_members, get_class_schedule
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt


app = Flask(__name__)
bcrypt = Bcrypt(app)

# Setup the Flask app configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@127.0.0.1:5050/gym_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

# Initialize the database
db.init_app(app)
migrate = Migrate(app, db)

# Context Processor to pass the current year to all templates
@app.context_processor
def inject_current_year():
    current_year = datetime.now().year
    return {'current_year': current_year}




class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    FullName = db.Column(db.String(100), nullable=False)
    Username = db.Column(db.String(100), unique=True, nullable=False)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    Password = db.Column(db.String(200), nullable=False)
    Role = db.Column(db.String(50), nullable=False)
    Status = db.Column(db.String(20), default='Active')




# Model for the 'members' table
class Member(db.Model):
    __tablename__ = 'members'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    member_weight = db.Column(db.Float, nullable=False)
    membership_id = db.Column(db.Integer, nullable=False)
    schedule_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(10), nullable=False)

# Model for the 'memberships' table
class Membership(db.Model):
    __tablename__ = 'memberships'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    membership_type = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    duration = db.Column(db.Integer, nullable=False)

@app.route('/')
def index():
    current_year = datetime.now().year
    return render_template('dashboard/index.html', year=current_year)

# Route for displaying memberships and handling forms
@app.route('/memberships', methods=['GET', 'POST'])
def memberships():
    if request.method == 'POST':
        membership_data = {
            "membership_type": request.form.get('MembershipType', '').strip(),
            "price": float(request.form.get('Price', 0)),
            "duration": int(request.form.get('Duration', 0))
        }

        # Validate data
        if not membership_data["membership_type"] or membership_data["price"] <= 0 or membership_data["duration"] <= 0:
            flash('Please ensure all fields are filled correctly.', 'danger')
            return redirect(url_for('memberships'))

        try:
            if request.form.get('membershipid') == 'insert':
                # Insert new membership record into database
                new_membership = Membership(**membership_data)
                db.session.add(new_membership)
                db.session.commit()  # Commit the changes
                flash('Successfully inserted!', 'success')
                return redirect(url_for('memberships'))
        except Exception as e:
            db.session.rollback()  # Rollback on error
            flash(f'Error occurred: {str(e)}', 'danger')  # Display error message


    elif request.form.get('membershipid') == 'update':
            membership = Membership.query.get(request.form.get('membership_Id'))
            if membership:
                for key, value in membership_data.items():
                    setattr(membership, key, value)
                db.session.commit()
                flash('Successfully updated!', 'success')
            else:
                flash('Membership not found.', 'danger')

# Fetch all memberships after any operation (GET or successful POST)
    memberships_list = Membership.query.all()  # Re-fetch updated list of memberships
    return render_template('memberships.html', memberships=memberships_list)

# Route for deleting a membership
@app.route('/delete_membership', methods=['POST'])
def delete_membership():
    membership_id = request.form.get('membership_id')
    membership = Membership.query.get(membership_id)
    if membership:
        db.session.delete(membership)
        db.session.commit()
        flash('Successfully Deleted!', 'success')
    else:
        flash('Membership not found or already deleted.', 'danger')
    return redirect(url_for('memberships'))


# Route for displaying members and handling forms
@app.route('/members', methods=['GET', 'POST'])
def members():
    if request.method == 'POST':
        member_data = {
            "full_name": request.form['FullName'].strip(),
            "date_of_birth": datetime.strptime(request.form['DateOfBirth'], '%Y-%m-%d'),
            "gender": request.form['Gender'].strip(),
            "phone": request.form['Phone'].strip(),
            "email": request.form['Email'].strip(),
            "address": request.form['Address'].strip(),
            "member_weight": float(request.form['MemberWeight']),
            "membership_id": int(request.form['MembershipID']),
            "schedule_id": int(request.form['schedule_id']),
            "status": request.form['Status'].strip(),
        }
        
        if request.form['TypeOfData'] == 'insert':
            new_member = Member(**member_data)
            db.session.add(new_member)
            db.session.commit()
            flash('Successfully inserted!', 'success')
        elif request.form['TypeOfData'] == 'update':
            member = Member.query.get(request.form['member_Id'])
            for key, value in member_data.items():
                setattr(member, key, value)
            db.session.commit()
            flash('Successfully updated!', 'success')

    members_list = Member.query.all()
    return render_template('/members.html', members=members_list)

# Route for deleting a member
@app.route('/delete_member', methods=['POST'])
def delete_member():
    member_id = request.form['member_id']
    member = Member.query.get(member_id)
    if member:
        db.session.delete(member)
        db.session.commit()
        flash('Successfully Deleted!', 'success')
    else:
        flash('Sorry! Something went wrong', 'danger')
    return redirect(url_for('members'))

@app.route('/schedule')
def schedule():
    return render_template('schedule.html')

@app.route('/trainers')
def trainers():
    return render_template('trainers.html')

@app.route('/classes')
def classes():
    return render_template('classes.html')

@app.route('/equipments')
def equipments():
    return render_template('equipments.html')

@app.route('/charges')
def charges():
    return render_template('charges.html')

@app.route('/income')
def income():
    return render_template('income.html')   

@app.route('/bank')
def bank():
    return render_template('bank.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/users')
def users():
    users_list = User.query.all()
    return render_template('users.html', users=users_list)
@app.route('/users/add', methods=['POST'])
def add_user():
    if request.method == 'POST':
        full_name = request.form.get('FullName').strip()
        username = request.form.get('Username').strip()
        email = request.form.get('Email').strip()
        password = bcrypt.generate_password_hash(request.form.get('Password')).decode('utf-8')
        role = request.form.get('Role').strip()
        status = request.form.get('Status').strip()
        new_user = User(
            FullName=full_name, Username=username, Email=email, Password=password, Role=role, Status=status
        )

        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('User successfully inserted!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')

    return redirect(url_for('users'))
@app.route('/users/update/<int:user_id>', methods=['POST'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        user.full_name = request.form.get('FullName').strip()
        user.username = request.form.get('Username').strip()
        user.email = request.form.get('Email').strip()
        user.password = bcrypt.generate_password_hash(request.form.get('Password')).decode('utf-8')
        user.role = request.form.get('Role').strip()
        user.status = request.form.get('Status').strip()

        try:
            db.session.commit()
            flash('User successfully updated!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')

    return redirect(url_for('users'))
@app.route('/users/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    try:
        db.session.delete(user)
        db.session.commit()
        flash('User successfully deleted!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')

    return redirect(url_for('users'))



@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')

if __name__ == '__main__':
    app.run(debug=True, port=5003)
