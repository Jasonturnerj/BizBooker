""" Models for databses"""
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

bcrypt = Bcrypt()
db = SQLAlchemy()

#Users table in the database
class Users(db.Model):
    __tablename__ = 'Users'

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

    image_url = db.Column(
        db.Text,
        default="",
    )

    bio = db.Column(
        db.Text,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )


    #business side of the table
    class business(db.Model):
        __tablename__ = 'businesses'
        
        id = db.Column(
        db.Integer,
        primary_key=True,
    )
        
        owner_id = db.Column(
        db.Integer,
        db.Foreignkey('Users.id')
    )

        location = db.Column(
        db.Text,
    )
        bio = db.Column(
        db.Text,
    )
        image_url = db.Column(
        db.Text,
        default="",
    )
    class appointment(db.Model):
        __tablename__ = 'appointments'

        id = db.Column(
            db.Integer,
            primary_key=True,
        
        )

        date_of_apt = db.Column(
            db.Datefield,
            Nullable=False
        )

        start_time = db.Column(
            db.Timefield,
            nullable=False,
        )



    @classmethod
    def signup(cls, username, email, password, image_url):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = Users(
                username=username,
                email=email,
                password=hashed_pwd,
                image_url=image_url,
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
    

    #I need to make a classmethod to check for autheticatign user id and password for business
    
def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)