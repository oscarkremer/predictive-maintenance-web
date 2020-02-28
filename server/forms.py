from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from server.models import User, Company
from wtforms import StringField, SelectField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from server import bcrypt


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    company = SelectField(u'Company', choices=[('Garten Automation', 'Garten Automation')])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField(
        'Confirm Password', validators=[
            DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RaspberryForm(FlaskForm):
    user = SelectField(u'User', choices=[('', '')])
    submit = SubmitField('Add Data Quality Equipment')

class AccountUpdateForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')
    
    def validate_username(self, username):
        if username.data != current_user.username:
            user_query = User.query.filter_by(username=username.data).first()
            if user_query:
                raise ValidationError(
                    'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user_query = User.query.filter_by(email=email.data).first()
            if user_query:
                raise ValidationError(
                    'That email is taken. Please choose a different one.')


class PasswordUpdateForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired(), Length(min=8, max=20)])
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField(
        'Confirm New Password', validators=[
            DataRequired(), EqualTo('password')])
    submit = SubmitField('Update')

    def user(self, user):
        self.user = user

    def validate_old_password(self, old_password):
        if not bcrypt.check_password_hash(self.user.password, old_password.data):
            raise ValidationError('Wrong Old Password, try again.')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    company = SelectField(u'Company', choices=[('Garten Automation', 'Garten Automation')])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    checked = BooleanField('Authenticate Account')
    admin = BooleanField('Administration Account')
    super_admin = BooleanField('Garten Administration Account')
    submit = SubmitField('Update')
    
    def user(self, user):
        self.user = user

    def validate_username(self, username):
        if username.data != self.user.username:
            user_query = User.query.filter_by(username=username.data).first()
            if user_query:
                raise ValidationError(
                    'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != self.user.email:
            user_query = User.query.filter_by(email=email.data).first()
            if user_query:
                raise ValidationError(
                    'That email is taken. Please choose a different one.')
    
class AnalysisForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    picture_1 = FileField('Insert Analysis Image', validators=[DataRequired(), 
                        FileAllowed(['jpg', 'png'])])
    picture_2 = FileField('Insert Analysis Image', validators=[DataRequired(), 
                        FileAllowed(['jpg', 'png'])])
    picture_3 = FileField('Insert Analysis Image', validators=[DataRequired(), 
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Analysis')

class CompanyForm(FlaskForm):
    name = StringField('Company Name',
                           validators=[DataRequired(), Length(min=2, max=100)])
    address = StringField('Address',
                           validators=[DataRequired(), Length(min=2, max=100)])
    city = StringField('City',
                           validators=[DataRequired(), Length(min=2, max=100)])
    country = StringField('Country',
                           validators=[DataRequired(), Length(min=2, max=100)])
    telephone = StringField('Telephone for Contact',
                           validators=[DataRequired(), Length(min=2, max=100)])
    picture = FileField('Add Company Picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('New Company')
  
    def validate_name(self, name):
        company = Company.query.filter_by(name=name.data).first()
        if company:
            raise ValidationError(
                'That username is taken. Please choose a different one.')

class UpdateCompanyForm(FlaskForm):
    name = StringField('Company Name',
                           validators=[DataRequired(), Length(min=2, max=100)])
    address = StringField('Address',
                           validators=[DataRequired(), Length(min=2, max=100)])
    city = StringField('City',
                           validators=[DataRequired(), Length(min=2, max=100)])
    country = StringField('Country',
                           validators=[DataRequired(), Length(min=2, max=100)])
    telephone = StringField('Telephone for Contact',
                           validators=[DataRequired(), Length(min=2, max=100)])
    picture = FileField('Add Company Picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('New Company')

    def company(self, company):
        self.company = company
    
    def validate_name(self, name):
        if name.data != self.company.name:
            company_query = Company.query.filter_by(name=name.data).first()
            if company_query:
                raise ValidationError(
                    'There is a company already registered with this name. Please choose a different one.')
        
class UpdateAnalysisForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    comment = StringField('Comment')
    submit = SubmitField('Analysis')

class SearchForm(FlaskForm):
    text = StringField('')
    title = BooleanField('Search by Title')
    user = BooleanField('Search by Username')
    company = BooleanField('Search by Company Name')
    submit = SubmitField('Search')
    