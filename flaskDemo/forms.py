from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, validators #DateField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from flaskDemo.models import Users
from datetime import date


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=25)])
    email = StringField('Email',
                        validators=[DataRequired(),Length(min=2, max=50), Email()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=6, max=15)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    firstName = StringField('First Name',
                        validators=[DataRequired(),Length(min=2, max=50)])
    lastName = StringField('Last Name',
                        validators=[DataRequired(),Length(min=2, max=50)])
    birthDate = DateField('Birthdate',
                        validators=[DataRequired()])
    gender = SelectField('Gender',
                        choices=[('M','Male'),('F','Female')],
                        validators=[DataRequired()])
    phone = StringField('Phone',
                        validators=[DataRequired(),Length(min=10, max=10)])
    address = StringField('Address',
                        validators=[DataRequired(),Length(min=2, max=100)])
    zipcode = StringField('Zip Code',
                        validators=[DataRequired(),Length(min=5, max=5)])
    city = StringField('City',
                        validators=[DataRequired(),Length(min=2, max=50)])
    insurancePro = StringField('Insurance Provider',
                        validators=[Optional(),Length(min=2, max=50)])
    insuranceNum = StringField('Insurance Number',
                        validators=[Optional(),Length(min=2, max=20)])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=25)])
    email = StringField('Email',
                        validators=[DataRequired(), Length(min=2, max=50), Email()])
    #picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    phone = StringField('Phone',
                        validators=[DataRequired(),Length(min=10, max=10)])
    address = StringField('Address',
                        validators=[DataRequired(),Length(min=2, max=100)])
    zipcode = StringField('Zip Code',
                        validators=[DataRequired(),Length(min=5, max=5)])
    city = StringField('City',
                        validators=[DataRequired(),Length(min=2, max=50)])
    insurancePro = StringField('Insurance Provider',
                        validators=[Optional(),Length(min=2, max=50)])
    insuranceNum = StringField('Insurance Number',
                        validators=[Optional(),Length(min=2, max=20)])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = Users.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')
        return self

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
        return self


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class TestDateForm(FlaskForm):
    testDate = DateField('Date', validators=[DataRequired()])
    submit = SubmitField('Select')

class InfoForm(FlaskForm):
    startdate = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    enddate = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit')
