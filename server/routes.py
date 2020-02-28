import os
import cv2
import secrets
import numpy as np
import pandas as pd
import time
from datetime import datetime, date
from PIL import Image
from sqlalchemy import desc
from flask import render_template, url_for, flash, redirect, request, abort, send_file, make_response
from flask_login import login_user, current_user, logout_user, login_required
from server import app, celery, db, bcrypt
from server.forms import *
from server.models import User, Analysis, Company, Raspberry
from src.utils import Path
from src.report import Report
from src.api.cerberus import classification
from src.utils.analytics import from_database
from celery.task.control import inspect

@app.route("/")
def open():
    return render_template('open.html')

@login_required
@app.route("/manual")
def manual():
    response = make_response(send_file('static/docs/manual.pdf', mimetype='application  /pdf'))
    response.headers['Content-Disposition'] = 'inline'
    return response

@login_required
@app.route("/referencial")
def referencial():
    response = make_response(send_file('static/docs/referencial.pdf', mimetype='application  /pdf'))
    response.headers['Content-Disposition'] = 'inline'
    return response

@app.route("/register", methods=['GET', 'POST'])
def register():
    companies = Company.query.order_by(desc('name')).all()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    form.company.choices = []
    for company in companies:
        form.company.choices.append((company.name, company.name))
    if form.validate_on_submit():
        company = Company.query.filter_by(name=form.company.data).first()
        if User.query.order_by(desc('id')).all():
            client_number = 1 + User.query.order_by(desc('id')).all()[0].id
            super_admin, admin, checked = False, False, False
        else:
            client_number = 1
            super_admin, admin, checked = True, True, True
        os.makedirs('data/client/{}'.format(client_number))
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data, company_id=company.id,
            email=form.email.data, password=hashed_password, admin=admin, super_admin=super_admin, checked=check)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form, companies=companies)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if user.checked:
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(
                    url_for('home'))
            else:
                flash('Login Unsuccessful. Waiting to be accepted', 'danger')
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('open'))

@app.route("/help")
def help():
    return render_template('help.html', title='Login')

@app.route('/request-data', methods=['GET','POST'])
def request_data():
    pi_data = request    
    if pi_data.values['conf'] == 'test':
        return 'Test-Connection'
    else:    
        equipment = Raspberry.query.filter_by(password=pi_data.values['key']).all()[0]
        if Analysis.query.order_by(desc('id')).all():
            analysis_number = 1 + Analysis.query.order_by(desc('id')).all()[0].id
        else:
            analysis_number = 1
        path = Path(equipment.owner.id, analysis_number)
        for v,i in pi_data.files.items():
            pi_data.files[v].save('{0}/{1}/{2}.jpg'.format(path.image_raw, v.split('_')[0], v.split('_')[1]))
        for folder in os.listdir(path.image_raw):
            for filename in os.listdir('{0}/{1}'.format(path.image_raw, folder)):
                image = cv2.imread('{0}/{1}/{2}'.format(path.image_raw, folder, filename))
                cv2.imwrite('{0}/{1}/{2}'.format(path.image_raw, folder, filename), cv2.flip(cv2.transpose(image, image), 1))
        analysis = Analysis(title='Cerberus - Analise - {}'.format(analysis_number), user_id=equipment.owner.id, company_id = equipment.owner.company.id, raspberry_id=equipment.id)
        db.session.add(analysis)
        db.session.commit()
        process.delay(analysis_number)

@login_required
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = SearchForm()
    analysiss = Analysis.query.filter_by(user_id=current_user.id, deleted=False).order_by(desc('date_posted')).all()
    if request.method == 'POST':
        search_analysis = []
        for analysis in analysiss:
            if form.text.data.lower() in analysis.title.lower():
                search_analysis.append(analysis)
    elif request.method == 'GET':
        search_analysis = analysiss
    if analysiss:
        return render_template('home.html', analysiss=search_analysis, form=form)
    else:
        return render_template('start.html')


@login_required
@app.route("/companies")
def companies():
    if current_user.super_admin:
        companies = Company.query.order_by(desc('id')).all()
        return render_template('companies.html', companies=companies)
    else:
        if current_user.admin:
            users = User.query.filter_by(
                company_id=current_user.company_id).all()
            return render_template('users.html', users=users)
        else:
            return redirect(url_for('activity'))

@login_required
@app.route("/company/<int:company_id>", methods=['GET', 'POST'])
def company(company_id):
    reference_dataframe = pd.DataFrame()
    info_dataframe = pd.DataFrame()
    company = Company.query.filter_by(id=company_id).all()[0]
    if current_user.super_admin:
        analysiss = Analysis.query.filter_by(
            company_id = company.id).order_by(
            desc('date_posted')).all()
        if analysiss:
            analysis_made = []
            start_analysis = analysiss[-1].date_posted
            end_analysis = analysiss[0].date_posted
            start_date = date(year = start_analysis.year, month = start_analysis.month, day = start_analysis.day)
            end_date = date(year = end_analysis.year, month = end_analysis.month, day = end_analysis.day)
            axis_timeseries = list(map(lambda x: x.date(), pd.date_range(start_date, end_date).tolist()))
            for analysis in analysiss:
                date_info =  analysis.date_posted
                analysis_made.append(date(year = date_info.year, month = date_info.month, day = date_info.day))
            info_dataframe['date'] = analysis_made
            info_dataframe['amount'] = np.ones(len(analysis_made))
            reference_dataframe['date'] = axis_timeseries
            reference_dataframe['amount'] = np.zeros(len(axis_timeseries))
            frames = [info_dataframe, reference_dataframe]
            result = pd.concat(frames)
            result = result.groupby(['date'], as_index=False).sum()
        else:
            result = pd.DataFrame()
            result['date'], result['amount'] = [], []
        form = UpdateCompanyForm()
        form.company(company)
        if request.method == 'POST':
            if form.validate_on_submit():
                if form.picture.data:
                    picture_file = save_picture(form.picture.data, path='company_pics')
                    company.image_file = picture_file
                company.name = form.name.data
                company.address = form.address.data
                company.city = form.city.data
                company.country = form.country.data
                company.telephone = form.telephone.data
                db.session.commit()
                flash('The Company Information has been Updated!', 'success')
                return redirect(url_for('company', company_id=company.id))
            flash('Error, please check the added information', 'danger')
        elif request.method == 'GET':
            form.name.data = company.name
            form.address.data = company.address
            form.city.data = company.city
            form.country.data = company.country
            form.telephone.data = company.telephone      
            image_file = url_for('static', filename='company_pics/' + company.image_file)
        return render_template('company.html', company=company, analysiss=analysiss, form=form,
            timeseries_values = result['amount'].values, timeseries_labels=result['date'].values)
    else:
        flash('You are not Allowed to Access this Information', 'danger')
        return redirect(url_for('home'))    

@app.route("/board/new", methods=['GET', 'POST'])
@login_required
def new_equipment():
    form = RaspberryForm()
    users = User.query.order_by(desc('username')).all()
    form.user.choices = []
    for user in users:
        form.user.choices.append((user.username, user.username))
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.user.data).first()
            raspberry = Raspberry(user_id=user.id, password=secrets.token_hex(8))
            db.session.add(raspberry)
            db.session.commit()
            flash('A new equipment has been registered!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Error, please check the added information', 'danger')
    return render_template('create_equipment.html', title='New Board',
                           form=form, legend='New Board')

@login_required
@app.route("/equipments", methods=['GET', 'POST'])
def equipments():
    search_equipments = []
    form = SearchForm()
    if current_user.super_admin:
        equipments = Raspberry.query.order_by(desc('user_id')).all()
        if request.method == 'POST':
            for equipment in equipments:
                added = False
                if form.user.data:
                    if form.text.data.lower() in equipment.owner.username.lower():
                        search_equipments.append(equipment) 
                        added = True
                if form.company.data:
                    if form.text.data.lower() in equipment.owner.company.name.lower() and not added:
                        search_equipments.append(equipment)                             
        else:
            search_equipments = equipments
            form.user.data = True
        return render_template('equipments.html', equipments=search_equipments, form=form)
    else:
        flash('You are not Allowed to Access this Information', 'danger')
        return redirect(url_for('home'))

@login_required
@app.route("/equipment/<int:equipment_id>", methods=['GET', 'POST'])
def equipment(equipment_id):
    equipment = Raspberry.query.filter_by(id=equipment_id).all()[0]
    if current_user.super_admin:
        form = RaspberryForm()
        users = User.query.filter_by(company_id=equipment.owner.company_id).order_by(desc('company_id')).all()
        form.user.choices = []
        form.user.choices.append((equipment.owner.username, equipment.owner.username))
        for user in users:
            if equipment.owner.username != user.username:
                form.user.choices.append((user.username, user.username))
        if request.method == 'POST':
            if form.validate_on_submit():
                user = User.query.filter_by(username=form.user.data).all()[0]
                equipment.user_id = user.id
                db.session.commit()
                flash('This Equipment has been updated!', 'success')
                return redirect(url_for('equipment', equipment_id=equipment.id))
            else:
                flash('Error, check the information', 'danger')
        elif request.method == 'GET':
            pass
        return render_template('equipment.html', equipment=equipment, form=form)
    else:
        flash('You are not allowed to access this information', 'danger')
        return redirect(url_for('home'))

@login_required
@app.route("/users", methods=['GET', 'POST'])
def users():
    search_users = []
    form = SearchForm()
    if current_user.super_admin:
        users = User.query.order_by(desc('company_id')).all()
    else:
        if current_user.admin:        
            users = User.query.filter_by(company_id=current_user.company_id).order_by(desc('company_id')).all()
        else:
            flash('You are not Allowed to Access this Information', 'danger')
            return redirect(url_for('home'))
    if request.method == 'POST':
        for user in users:
            added = False
            if form.user.data:
                if form.text.data.lower() in user.username.lower():
                    search_users.append(user)
                    added = True
            if form.company.data:
                if form.text.data.lower() in user.company.name.lower() and not added:
                    search_users.append(user)                             
    else:
        search_users = users
        form.user.data = True
    if current_user.super_admin:
        return render_template('users.html', users=search_users, form = form)
    else:
        if current_user.admin:
            users = User.query.filter_by(
                company_id=current_user.company_id).all()
            return render_template('users.html', users=search_users, form = form)
        else:
            return redirect(url_for('activity'))

@login_required
@app.route("/user/<int:user_id>", methods=['GET', 'POST'])
def user(user_id):
    user = User.query.filter_by(id=user_id).all()[0]
    if current_user.super_admin or (current_user.admin and (current_user.company.id==user.company.id)):
        analysiss = Analysis.query.filter_by(user_id=user_id).order_by(desc('date_posted')).all()
        form = UpdateAccountForm()
        form.user(user)
        companies = Company.query.order_by(desc('name')).all()
        form.company.choices = []
        form.company.choices.append((user.company.name, user.company.name))
        for company in companies:
            if company.name != user.company.name:
                form.company.choices.append((company.name, company.name))
        if request.method == 'POST':
            if form.validate_on_submit():
                if form.picture.data:
                    picture_file = save_picture(form.picture.data)
                    user.image_file = picture_file
                user.username = form.username.data
                user.email = form.email.data  
                user.checked = form.checked.data  
                user.admin = form.admin.data  
                user.company =  Company.query.filter_by(name=form.company.data).first()
                user.super_admin = form.super_admin.data              
                db.session.commit()
                flash('Your account has been updated!', 'success')
                return redirect(url_for('user', user_id=user.id))
            else:
                flash('Error, please check the added information', 'danger')
        elif request.method == 'GET':
            form.username.data = user.username
            form.email.data = user.email
            form.checked.data = user.checked
            form.admin.data = user.admin
            form.super_admin.data = user.super_admin
        image_file = url_for('static', filename='/profile_pics/'+current_user.image_file)
        if current_user.super_admin:
            return render_template('user.html', user=user, analysiss=analysiss, form=form)
        else:
            return render_template('user_analysis.html', user=user, analysiss=analysiss)
    else:
        flash('You are not allowed to access this information', 'danger')
        return redirect(url_for('home'))

@app.route("/download_report/<int:analysis_id>")
@login_required
def download_report(analysis_id):
    report_name = 'report.pdf'
    report = Report()
    analysis = Analysis.query.get_or_404(analysis_id)      
    if (current_user.admin and (current_user.company.id==analysis.company_id)) or analysis.user_id == current_user.id or current_user.super_admin:
        path = Path(analysis.author.id, analysis.id)
        image_file = 'server/static/profile_pics/' + analysis.author.image_file
        report.create_report(path.report, image_file, analysis)
        return send_file('{0}/{1}'.format(path.report, report_name),
                            mimetype='text/pdf',
                            attachment_filename=report_name,
                            as_attachment=True)
                            
@login_required
@app.route("/activity")
def activity():
    reference_dataframe = pd.DataFrame()
    info_dataframe = pd.DataFrame()
    analysis = Analysis.query.filter_by(
            user_id=current_user.id).order_by(
            desc('date_posted')).all()
    if analysis:
        analysis_made = []
        start_analysis = analysis[-1].date_posted
        end_analysis = analysis[0].date_posted
        start_date = date(year = start_analysis.year, month = start_analysis.month, day = start_analysis.day)
        end_date = date(year = end_analysis.year, month = end_analysis.month, day = end_analysis.day)
        axis_timeseries = list(map(lambda x: x.date(), pd.date_range(start_date, end_date).tolist()))
        for analyse in analysis:
            date_info =  analyse.date_posted
            analysis_made.append(date(year = date_info.year, month = date_info.month, day = date_info.day))
        info_dataframe['date'] = analysis_made
        info_dataframe['amount'] = np.ones(len(analysis_made))
        reference_dataframe['date'] = axis_timeseries
        reference_dataframe['amount'] = np.zeros(len(axis_timeseries))
        frames = [info_dataframe, reference_dataframe]
        result = pd.concat(frames)
        result = result.groupby(['date'], as_index=False).sum()
        return render_template('activity.html', title='Activity', user=current_user, 
                                timeseries_values = result['amount'].values, timeseries_labels=result['date'].values)
    else:
        return render_template('start.html', title='Activity')

@login_required
@app.route("/about", methods=['GET', 'POST'])
def about():
    return render_template('about.html', title='About')

@login_required
@app.route("/progress")
def progress():
    return render_template('progress.html', title='Progress')

@app.route("/reanalysis/<int:analysis_id>")
@login_required
def reanalysis(analysis_id):
    analysis = Analysis.query.get_or_404(analysis_id)
    if analysis.user_id == current_user.id or current_user.super_admin or (current_user.admin and current_user.company_id==analysis.company_id):
        analysis.state = False
        db.session.commit()
        process.delay(analysis_id)
    return redirect(url_for('home'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = AccountUpdateForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                current_user.image_file = picture_file
            current_user.username = form.username.data
            current_user.email = form.email.data       
            db.session.commit()
            flash('Your account has been updated!', 'success')
            return redirect(url_for('account'))
        else:
            flash('Error, please check the added information', 'danger')
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        'static',
        filename='profile_pics/' +
        current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

@app.route("/account/advanced/<int:user_id>", methods=['GET', 'POST'])
@login_required
def account_advanced(user_id):
    form = PasswordUpdateForm()
    user = User.query.filter_by(id=user_id).all()[0]
    form.user(user)
    if request.method == 'POST':
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(
                form.password.data).decode('utf-8')
            current_user.password = hashed_password
            db.session.commit()
            flash('Your Password has been updated!', 'success')
            return redirect(url_for('account'))
        else:
            flash('Error, please check the added information', 'danger')
    return render_template('account_advanced.html', title='Account', form=form)


@app.route("/company/new", methods=['GET', 'POST'])
@login_required
def new_company():
    form = CompanyForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if form.picture.data:
                picture_file= save_picture(form.picture.data, path='company_pics')
                company = Company(name=form.name.data, address=form.address.data, country=form.country.data,
                    city = form.city.data, telephone = form.telephone.data, image_file=picture_file)
            else:
                company = Company(name=form.name.data, address=form.address.data, country=form.country.data,
                    city = form.city.data, telephone = form.telephone.data)
            db.session.add(company)
            db.session.commit()
            flash('A new company has been registered!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Error, please check the added information', 'danger')
    return render_template('create_company.html', title='New Company',
                           form=form, legend='New Company')

@app.route("/analysis/new", methods=['GET', 'POST'])
@login_required
def new_analysis():
    form = AnalysisForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            pictures = [Image.open(form.picture_1.data), Image.open(form.picture_2.data), 
                    Image.open(form.picture_3.data)]
            if Analysis.query.order_by(desc('id')).all():
                analysis_number = 1 + Analysis.query.order_by(desc('id')).all()[0].id
            else:
                analysis_number = 1
            path = Path(current_user.id, analysis_number)
            for index, picture in enumerate(pictures):
                picture.save('{0}/{1}.jpg'.format(path.white_raw, index+1))
            src_gray = cv2.blur(src_gray, (3, 3))

            analysis = Analysis(title=form.title.data, user_id=current_user.id, company_id=current_user.company_id)
            db.session.add(analysis)
            db.session.commit()
            process.delay(analysis_number)
            flash('Your Analysis has been created!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Only .jpg files can be used', 'danger')
    return render_template('create_analysis.html', title='New Analysis',
                           form=form, legend='New Analysis')

@login_required
@app.route("/analysis/<int:analysis_id>")
def analysis(analysis_id):
    analysis = Analysis.query.get_or_404(analysis_id)
    if analysis.deleted:
        return render_template('deleted.html', analysis=analysis)
    elif analysis.user_id == current_user.id or current_user.super_admin or (analysis.company_id==current_user.company_id and current_user.admin):
        if analysis.state:
            if analysis.error:
                return render_template('error.html', analysis=analysis)
            else:
                colors = [
                    "#006666", "#333333", "#009999", "#669999", "#98FB98",
                    "#666666", "#999999", "#CCCCCC"]  
                problems, geometric = from_database(analysis)
                return render_template(
                    'analysis.html',
                    title=analysis.title,
                    analysis=analysis,
                    max=105,
                    problem_labels=problems['type'].values,
                    problem_values=problems['quantity'].values,
                    geometric_labels=geometric['type'].values,
                    geometric_values=geometric['quantity'].values,
                    colors=colors)
        else:
            return render_template('progress.html', title='Progress')
    else:
        flash('Analysis not vinculated with this user id', 'danger')
        return redirect(url_for('home'))

@app.route("/analysis/<int:analysis_id>/update", methods=['GET', 'POST'])
@login_required
def update_analysis(analysis_id):
    analysis = Analysis.query.get_or_404(analysis_id)
    if analysis.author != current_user:
        abort(403)
    form = UpdateAnalysisForm()
    if form.validate_on_submit():
        analysis.title = form.title.data
        analysis.comment = form.comment.data
        db.session.commit()
        flash('Your analysis has been updated!', 'success')
        return redirect(url_for('analysis', analysis_id=analysis.id))
    elif request.method == 'GET':
        form.title.data = analysis.title
    return render_template('update_analysis.html', title='Update Analysis',
                           form=form, legend='Update Analysis')

@app.route("/analysis/<int:analysis_id>/delete", methods=['POST'])
@login_required
def delete_analysis(analysis_id):
    analysis = Analysis.query.get_or_404(analysis_id)
    if analysis.author != current_user:
        abort(403)
    analysis.deleted = True
    db.session.commit()
    flash('Your Analysis has been deleted!', 'success')
    return redirect(url_for('home'))

def save_picture(form_picture, path='profile_pics'):
    output_size = (125, 125)
    pictures = Image.open(form_picture) 
    _, file_extension = os.path.splitext(form_picture.filename)
    random_hex = secrets.token_hex(8)
    try:
        pictures.thumbnail(output_size).save('server/static/{0}/{1}{2}'.format(path,random_hex, file_extension))
    except:
        pictures.save('server/static/{0}/{1}{2}'.format(path,random_hex, file_extension))
    return '{0}{1}'.format(random_hex, file_extension)
    
@celery.task(name="routes.process", bind=True)
def process(self, analysis_id):
    analysis = Analysis.query.get_or_404(analysis_id)
    try:
        if not analysis.state:
            problems, geometric, empty, error = classification(analysis.user_id, analysis.id)   
            if not error:        
                analysis.total = problems['ardido&mofado']+problems['bandinha']+problems['saudavel']+problems['genetico']+problems['caruncho']+problems['mordido']+problems['manchado']+problems['contaminantes']
                analysis.ardido = float("{:0.2f}".format(100*problems['ardido&mofado']/analysis.total))
                analysis.bandinha = float("{:0.2f}".format(100*problems['bandinha']/analysis.total))
                analysis.saudavel = float("{:0.2f}".format(100*(problems['saudavel']-geometric['imaturo'].values[0])/analysis.total))
                analysis.genetico = float("{:0.2f}".format(100*problems['genetico']/analysis.total))
                analysis.caruncho = float("{:0.2f}".format(100*problems['caruncho']/analysis.total))
                analysis.mordido = float("{:0.2f}".format(100*problems['mordido']/analysis.total))
                analysis.manchado = float("{:0.2f}".format(100*problems['manchado']/analysis.total))
                analysis.imaturo = float("{:0.2f}".format(100*geometric['imaturo'].values[0]/analysis.total))                
                analysis.contaminantes = float("{:0.2f}".format(100*problems['contaminantes']/analysis.total))
                analysis.problemas = analysis.ardido + analysis.bandinha + analysis.genetico + analysis.caruncho + analysis.mordido + analysis.manchado + analysis.contaminantes + analysis.imaturo
                analysis.size_12 = float("{:0.2f}".format(100*(geometric['12'].values[0]/(analysis.total*analysis.saudavel/100))))
                analysis.size_11 = float("{:0.2f}".format(100*(geometric['11'].values[0]/(analysis.total*analysis.saudavel/100))))
                analysis.size_10 = float("{:0.2f}".format(100*(geometric['10'].values[0]/(analysis.total*analysis.saudavel/100))))
                analysis.size_9 = float("{:0.2f}".format(100*(geometric['9'].values[0]/(analysis.total*analysis.saudavel/100))))
                analysis.error = False
                analysis.error_fatal = False
                analysis.state = True
                analysis.empty = empty
            elif analysis.error:
                analysis.error_fatal, analysis.state = True, True
            else:
                analysis.error, analysis.state = True, True
            db.session.commit()
    except Exception as exc:
        print(exc)
        if analysis.error:
            analysis.error_fatal, analysis.state = True, True
            db.session.commit()
        else:
            analysis.error, analysis.state = True, True
            db.session.commit()
            raise self.retry(exc=exc)
            
