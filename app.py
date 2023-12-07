# TODO: Relate business to user
#       User to business view toggle

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

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""
    if CURR_USER_KEY in session:
        g.user = Users.query.get(session[CURR_USER_KEY])
        
    else:
        g.user = None

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/' , methods=['GET', 'POST'])
def homepage():
    """Show the homepage with a signup button."""
    return render_template('base.html')

@app.route('/homepage')
def home():
    """Show the homepage with a signup button."""
    return render_template('homepage.html')


@app.route('/signup', methods=["GET","POST"])
def signup():
    """User signup."""
    form = UserForm()

    if form.validate_on_submit():

        user = Users.signup(
            username=form.username.data,
            password=form.password.data,
            email=form.email.data,
            bio=form.bio.data
        )
        db.session.commit()

        return redirect('/login')
    
    return render_template('signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = Users.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/homepage")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """Handle logout of user."""
    do_logout()
    flash("Successfully Logged Out")
    return redirect("/login")

@app.route('/create', methods=['GET', 'POST'])
def create_business():
    """Create a new business."""
    form = BusinessForm()

    if form.validate_on_submit():
        # Create a new business
        business = Business(
            owner_id=session[CURR_USER_KEY],
            name=form.name.data,
            location=form.location.data,
            bio=form.bio.data,
        )
        db.session.add(business)
        db.session.update()
        db.session.commit()

        # Update the user's attribute
        user_id = session[CURR_USER_KEY]
        user = Users.query.get(user_id)
        if user:
            user.is_business_owner = True
            db.session.commit()

        return redirect('/homepage')

    return render_template('create.html', form=form)


# ...

@app.route('/businesses')
def list_businesses():
    """List all businesses."""
    businesses = Business.query.all()
    return render_template('list.html', businesses=businesses)



@app.route('/businesses/<int:business_id>')
def show_business(business_id):
    """Show details of a business and available appointments."""
    business = Business.query.get_or_404(business_id)
    appointments = Appointment.query.filter_by(business_id=business_id).all()

    return render_template('show.html', business=business, appointments=appointments)

@app.route('/appointments/<int:business_id>', methods=['GET', 'POST'])
def book_appointment(business_id):
    """Book an appointment for a specific business."""
    form = AppointmentForm()

    if form.validate_on_submit():
        # Create a new appointment
        new_appointment = Appointment(
            date_of_apt=form.date_of_apt.data,
            start_time=form.start_time.data,
            owner_id=session[CURR_USER_KEY],
            business_id=business_id
        )

        db.session.add(new_appointment)
        db.session.commit()

        flash('Appointment booked successfully!', 'success')
        return redirect(f'/businesses/{business_id}')

    return render_template('book.html', form=form)

@app.route('/view')
def view_appointments():
    """View appointments for the current user or business."""
    user_id = session.get(CURR_USER_KEY)

    if not user_id:
        flash('Please log in first.', 'danger')
        return redirect('/login')  # Redirect to login if not logged in

        # user = Users.query.get_or_404(user_id)
        # appointments = Appointment.query.filter((Appointment.owner_id == user.id) | (Appointment.business.id== user.id)).all()
    return render_template('view.html')


@app.route('/users/delete', methods=["POST"])
def delete_user():
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    return redirect("/signup")

connect_db(app)
if __name__ == "__main__":
    app.run(debug=True)