from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import PasswordField
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app import bcrypt
from app.models import User

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    telephone = StringField('Telephone',
                        validators=[DataRequired()])
    alarms = BooleanField('I want messages messages in case of any anomaly, in addition to daily reports.')
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

class AccountUpdateForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    telephone = StringField('Telephone',
                        validators=[DataRequired()])
    alarms = BooleanField('I want messages messages in case of any anomaly, in addition to daily reports.')
    submit = SubmitField('Update')
    def setUser(self, user):
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


