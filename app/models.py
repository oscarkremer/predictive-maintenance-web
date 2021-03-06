from flask_login import UserMixin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telephone = db.Column(db.String(20),unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    alarms = db.Column(db.Boolean, nullable=False)
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Measure(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    acel_x = db.Column(db.Float, nullable=False)
    down_acel_x = db.Column(db.Float, nullable=False)
    upper_acel_x = db.Column(db.Float, nullable=False)
    acel_y = db.Column(db.Float, nullable=False)
    down_acel_y = db.Column(db.Float, nullable=False)
    upper_acel_y = db.Column(db.Float, nullable=False)
    acel_z = db.Column(db.Float, nullable=False)
    down_acel_z = db.Column(db.Float, nullable=False)   
    upper_acel_z = db.Column(db.Float, nullable=False)
    rot_x = db.Column(db.Float, nullable=False)
    down_rot_x = db.Column(db.Float, nullable=False)
    upper_rot_x = db.Column(db.Float, nullable=False)   
    rot_y = db.Column(db.Float, nullable=False)
    down_rot_y = db.Column(db.Float, nullable=False)
    upper_rot_y = db.Column(db.Float, nullable=False)
    rot_z = db.Column(db.Float, nullable=False)
    down_rot_z = db.Column(db.Float, nullable=False)  
    upper_rot_z = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    down_temperature = db.Column(db.Float, nullable=False)
    upper_temperature = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    anomaly = db.relationship('Anomaly', backref='fault', lazy=True)
    def __repr__(self):
        return f"Measure"


class Anomaly(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    measure_id = db.Column(db.Integer, db.ForeignKey('measure.id'), nullable=False)
    variable = db.Column(db.String(30), nullable=False)
    behavior = db.Column(db.String(30), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    def __repr__(self):
        return f"Anomaly"

db.create_all()
