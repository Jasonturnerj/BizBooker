from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, DateField, TimeField
from wtforms.validators import DataRequired, Email , Length

class UserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    image_url = StringField('Image URL')
    bio = TextAreaField('Bio')
    password = PasswordField('Password', validators=[Length(min=6,max=10)])

class BusinessForm(FlaskForm):
    owner_id = IntegerField('Owner ID', validators=[DataRequired()])
    owner_username = StringField('Your Username', validators=[DataRequired()])
    owner_password = PasswordField('Your Password', validators=[DataRequired()])
    location = StringField('Location')
    bio = TextAreaField('Bio')
    image_url = StringField('Image URL')

class AppointmentForm(FlaskForm):
    date_of_apt = DateField('Date of Appointment', validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
