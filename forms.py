from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, DateField, TimeField
from wtforms.validators import DataRequired, Email , Length

class UserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6,max=10)])
    bio = TextAreaField('Bio')
    

class BusinessForm(FlaskForm):
    owner_username = StringField('Your Username', validators=[DataRequired()])
    owner_password = PasswordField('Your Password', validators=[DataRequired()])
    name = TextAreaField('Name')
    location = StringField('Location')
    bio = TextAreaField('Bio')
    

class AppointmentForm(FlaskForm):
    date_of_apt = DateField('Date of Appointment', validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    comment = TextAreaField('comment')

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class UserEditForm(FlaskForm):
    """Edit User Form"""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    image_url = StringField('(Optional) Image URL')
    header_image_url = StringField('(Optional) Header Image URL')
    bio = StringField('User Bio')
    password = PasswordField('Password')