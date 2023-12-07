""" Models for databses"""
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

bcrypt = Bcrypt()
db = SQLAlchemy()

#Users table in the database
class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    bio = db.Column(
        db.Text,
    )

    business_view = db.Column(
        db.Boolean,
        default=False
    )

    business = db.relationship('Business', backref='users', uselist=False)

    

    

    @classmethod
    def signup(cls, username, email, bio, password):
        """Sign up user.

            Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = Users(
                username=username,
                email=email,
                password=hashed_pwd,
                bio=bio
                )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

    #business side of the table
class Business(db.Model):
    __tablename__ = 'businesses'
    
    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    
    owner_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False,
        unique=True
    )

    name = db.Column(
        db.Text,
    )

    location = db.Column(
        db.Text,
    )
    bio = db.Column(
        db.Text,
    )
    appointments = db.relationship('Appointment', backref='business', lazy=True)
     
class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(
        db.Integer,
        primary_key=True,
    
    )

    date_of_apt = db.Column(
        db.Date,
        nullable=False
    )

    start_time = db.Column(
        db.Time,
        nullable=False,
    )
    comment = db.Column(
            db.Text,
    )

    owner_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )
    
    business_id = db.Column(
        db.Integer,
        db.ForeignKey('businesses.id'),
        nullable=False
    )





    

    #I need to make a classmethod to check for authetication user id and password for business
    
def connect_db(app):
    db.app = app
    db.init_app(app)