from flask import redirect
from flask import render_template
from flask import request, jsonify
from flask import url_for, flash
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from werkzeug.urls import url_parse
from app import app, db, bcrypt
from app.forms import *
from app.models import User
from sqlalchemy import desc
from time import sleep
import requests, json, atexit, time


@app.route('/')
def index():
    return render_template("index.html", title='Home Page')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(
                'http://127.0.0.1:8000/dashboard', code=302)
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/request-data', methods=['GET', 'POST'])
def request_data():
    pi_data = request.json
    try:
        if pi_data:
            print(pi_data)
            measure = Measure(acel_x=pi_data['AcX'], acel_y=pi_data['AcY'], acel_z=pi_data['AcZ'],
                temperature=pi_data['Temperature'], rot_x=pi_data['GyX'], rot_y=pi_data['GyY'],rot_z=pi_data['GyZ'])
            db.session.add(measure)
            db.session.commit()
            return jsonify(pi_data)
        else:
            return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'status': 'error'})
   
@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
            email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

