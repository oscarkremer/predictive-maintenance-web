from flask import redirect, render_template
from flask import request, jsonify, url_for, flash
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse
from app import app, db, bcrypt
from app.forms import *
from app.models import *
from sqlalchemy import desc
from time import sleep
import requests, json, atexit, time


@app.route("/")
def open():
    return render_template('open.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('http://0.0.0.0:8000/dashboard', code=302)
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(
                'http://0.0.0.0:8000/dashboard', code=302)
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/request-data', methods=['GET', 'POST'])
def request_data():
    pi_data = request.json
    try:
        if pi_data:
            try:
                print(pi_data)
                measure = Measure(acel_x=pi_data['AcX'], down_acel_x = pi_data['DownAcX'], upper_acel_x = pi_data['UpAcX'],
                    acel_y=pi_data['AcY'], down_acel_y = pi_data['DownAcY'], upper_acel_y = pi_data['UpAcY'],
                    acel_z=pi_data['AcZ'], down_acel_z = pi_data['DownAcZ'], upper_acel_z = pi_data['UpAcZ'],
                    rot_x=pi_data['GyX'], down_rot_x = pi_data['DownGyX'], upper_rot_x = pi_data['UpGyX'],
                    rot_y=pi_data['GyY'], down_rot_y = pi_data['DownGyY'], upper_rot_y = pi_data['UpGyY'],
                    rot_z=pi_data['GyZ'], down_rot_z = pi_data['DownGyZ'], upper_rot_z = pi_data['UpGyZ'],
                    temperature=pi_data['Tmp'], down_temperature = pi_data['DownTmp'], upper_temperature = pi_data['UpTmp'])
                db.session.add(measure)
                db.session.commit()
                return jsonify(pi_data)
            except Exception as e:
                print('error - {}'.format(e))
                return jsonify({'status': 'ok'})
        else:
            return jsonify({'status': 'ok'})
    except Exception as e:
        print('error - {}'.format(e))
        return jsonify({'status': 'error'})
   
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('http://0.0.0.0:8000')


@app.route('/register/', methods=['GET', 'POST'])
def register():
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

