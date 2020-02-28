from datetime import datetime
from server import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(100), unique=True, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(100), nullable=False)
    user = db.relationship('User', backref='company', lazy=True)
    analysis = db.relationship('Analysis', backref='company_author', lazy=True)
    image_file = db.Column(
        db.String(20),
        nullable=False,
        default='default.png')
    def __repr__(self):
        return f"Company('{self.name}')"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    checked = db.Column(db.Boolean, nullable=False, default=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    super_admin = db.Column(db.Boolean, nullable=False, default=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(
        db.String(20),
        nullable=False,
        default='default.png')
    password = db.Column(db.String(60), nullable=False)
    analysis = db.relationship('Analysis', backref='author', lazy=True)
    raspberry = db.relationship('Raspberry', backref='owner', lazy=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Raspberry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(60), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    analysis = db.relationship('Analysis', backref='equipment', lazy=True)
    def __repr__(self):
        return f"Raspberry('{self.id}', '{self.user_id}')"


class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.String(100), nullable=False, default='No comments')
    type_grain = db.Column(db.String(100), nullable=False, default='Feijão-Carioca')
    deleted = db.Column(db.Boolean, nullable=False, default=False)
    error = db.Column(db.Boolean, nullable=False, default=False)
    error_fatal = db.Column(db.Boolean, nullable=False, default=False)
    state = db.Column(db.Boolean, nullable=False, default=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    raspberry_id = db.Column(db.Integer, db.ForeignKey('raspberry.id'), nullable=True)
    saudavel = db.Column(db.Integer, nullable=False, default=0)
    problemas = db.Column(db.Integer, nullable=False, default=0)
    bandinha = db.Column(db.Integer, nullable=False, default=0)
    ardido = db.Column(db.Integer, nullable=False, default=0)
    caruncho = db.Column(db.Integer, nullable=False, default=0)
    mordido = db.Column(db.Integer, nullable=False, default=0)
    imaturo = db.Column(db.Integer, nullable=False, default=0)
    genetico = db.Column(db.Integer, nullable=False, default=0)
    manchado = db.Column(db.Integer, nullable=False, default=0)
    contaminantes = db.Column(db.Integer, nullable=False, default=0)
    total = db.Column(db.Integer, nullable=False, default=0)
    empty = db.Column(db.Integer, nullable=False, default=0)
    size_12 = db.Column(db.Integer, nullable=False, default=0)
    size_11 = db.Column(db.Integer, nullable=False, default=0)
    size_10 = db.Column(db.Integer, nullable=False, default=0)  
    size_9 = db.Column(db.Integer, nullable=False, default=0)  
    color = db.Column(db.Float, nullable=False, default=0)
    def __repr__(self):
        return f"Analysis('{self.title}', '{self.date_posted}')"
