import os

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate

from forms import UserForm, LoginForm, AppointmentForm, BusinessForm,UserEditForm
from models import db, connect_db, Users, Business, Appointment

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.app_context().push()
# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql://postgres:1122@localhost/bizbooker'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)
migrate = Migrate(app,db)


connect_db(app)
if __name__ == "__main__":
    app.run(debug=True)