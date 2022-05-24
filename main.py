from flask import Flask, render_template, redirect, url_for, flash, abort, request
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import RegisterForm, LoginForm, PreferenceForm, DestinationForm
from functools import wraps
from datetime import date, datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'
Bootstrap(app)

# LATER, during Heroku stage
# uri = os.getenv("DATABASE_URL")
# if uri and uri.startswith("postgres://"):
#     uri = uri.replace("postgres://", "postgresql://", 1)
# app.config['SQLALCHEMY_DATABASE_URI'] = uri

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///club-users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

Base = declarative_base()


class User(UserMixin, db.Model, Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(50))
    name = db.Column(db.String(100))
    preferences = relationship('Preferences', back_populates="user_pref")
    destinations = relationship('Destinations', back_populates="user_dest")
    flight_deals = relationship('FlightDeals', back_populates="user_deals")


class Destinations(db.Model, Base):
    __tablename__ = 'destinations'
    # id is for this table, same as all tables
    id = db.Column(db.Integer, primary_key=True)
    # relationship id uses ForeignKey with the table name of parent: (users)
    user_dest_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # relationship param uses the parent class name: (User)
    # back_populates to whatever you named the relationship in the parent/child
    user_dest = relationship("User", back_populates="destinations")
    home_airport = db.Column(db.String(50))
    city1 = db.Column(db.String(100))
    price1 = db.Column(db.Integer)
    city2 = db.Column(db.String(100))
    price2 = db.Column(db.Integer)
    city3 = db.Column(db.String(100))
    price3 = db.Column(db.Integer)
    city4 = db.Column(db.String(100))
    price4 = db.Column(db.Integer)
    city5 = db.Column(db.String(100))
    price5 = db.Column(db.Integer)
    city6 = db.Column(db.String(100))
    price6 = db.Column(db.Integer)
    city7 = db.Column(db.String(100))
    price7 = db.Column(db.Integer)
    city8 = db.Column(db.String(100))
    price8 = db.Column(db.Integer)
    city9 = db.Column(db.String(100))
    price9 = db.Column(db.Integer)
    city10 = db.Column(db.String(100))
    price10 = db.Column(db.Integer)
    destinations = []


class Preferences(db.Model, Base):
    __tablename__ = 'preferences'
    id = db.Column(db.Integer, primary_key=True)
    user_pref_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_pref = relationship("User", back_populates="preferences")
    email_frequency = db.Column(db.Integer)
    min_nights = db.Column(db.Integer, nullable=False)
    max_nights = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(50), nullable=False)
    cabin_class = db.Column(db.String(50), nullable=False)
    mix_class = db.Column(db.String(50))
    exclude_airlines = db.Column(db.String(100), nullable=False)
    flight_type = db.Column(db.String(100), nullable=False)
    max_stops = db.Column(db.Integer)
    max_flight_time = db.Column(db.Integer)
    num_adults = db.Column(db.Integer, nullable=False)
    num_children = db.Column(db.Integer, nullable=False)
    num_infants = db.Column(db.Integer, nullable=False)
    search_start_date = db.Column(db.String(200))
    specific_search_start_date = db.Column(db.Date)
    search_length = db.Column(db.String(200))
    specific_search_end_date = db.Column(db.Date)


class FlightDeals(db.Model, Base):
    __tablename__ = 'flightdeals'
    id = db.Column(db.Integer, primary_key=True)
    user_deals_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_deals = relationship("User", back_populates="flight_deals")
    deal1 = db.Column(db.String(1000))
    link1 = db.Column(db.String(1000))
    deal2 = db.Column(db.String(1000))
    link2 = db.Column(db.String(1000))
    deal3 = db.Column(db.String(1000))
    link3 = db.Column(db.String(1000))
    deal4 = db.Column(db.String(1000))
    link4 = db.Column(db.String(1000))
    deal5 = db.Column(db.String(1000))
    link5 = db.Column(db.String(1000))
    deal6 = db.Column(db.String(1000))
    link6 = db.Column(db.String(1000))
    deal7 = db.Column(db.String(1000))
    link7 = db.Column(db.String(1000))
    deal8 = db.Column(db.String(1000))
    link8 = db.Column(db.String(1000))
    deal9 = db.Column(db.String(1000))
    link9 = db.Column(db.String(1000))
    deal10 = db.Column(db.String(1000))
    link10 = db.Column(db.String(1000))

# db.create_all()


def admin_only(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.id != 1:
            return abort(403)
        else:
            return function(*args, **kwargs)

    return decorated_function


@login_manager.user_loader
def load_user(user_id):
    # print(user_id)

    return User.query.get(user_id)


@app.route('/')
def landing_page():
    return render_template("index.html", page_title="")


# @app.route('/new', methods=["GET","POST"])
# def new():
#     if request.method == "GET":
#         print("GET")
#     if request.method == "POST":
#         print("POST")
#         print(request.data)
#     page_title = "Page Title"
#     return render_template("new_register.html", page_title=page_title)


@app.route('/home')
@login_required
def user_home():
    user_name = current_user.name
    page_title = f"Hello, {user_name}"
    return render_template("user_home.html", page_title=page_title)


@app.route('/my_destinations')
@login_required
def my_destinations():
    page_title = "My Destinations"
    des = Destinations.query.filter_by(user_dest_id=current_user.id).first()
    return render_template("my_destinations.html", page_title=page_title, des=des)


@app.route('/update_destinations', methods=['GET', 'POST'])
@login_required
def update_destinations():
    page_title = "Update Destinations"
    # Grabs the current user object which contains their data
    user_des = Destinations.query.filter_by(user_dest_id=current_user.id).first()
    # Form obj below doesn't populate fields contained within the FieldList/FormField.
    # instead, need to manually add the data from the user object and pass it as a list of dictionaries
    # to the SQL table varable that matches the name of the FieldList variable in the form (ex: 'destinations)
    user_des.destinations = [{'city': user_des.city1, 'price_ceiling': user_des.price1},
                             {'city': user_des.city2, 'price_ceiling': user_des.price2},
                             {'city': user_des.city3, 'price_ceiling': user_des.price3},
                             {'city': user_des.city4, 'price_ceiling': user_des.price4},
                             {'city': user_des.city5, 'price_ceiling': user_des.price5},
                             {'city': user_des.city6, 'price_ceiling': user_des.price6},
                             {'city': user_des.city7, 'price_ceiling': user_des.price7},
                             {'city': user_des.city8, 'price_ceiling': user_des.price8},
                             {'city': user_des.city9, 'price_ceiling': user_des.price9},
                             {'city': user_des.city10, 'price_ceiling': user_des.price10}]
    # Get rid of empty destination so it doesn't show up on the form:
    # iterating through a list while deleting items from the list causes weird behavior
    # Used proxy method with removal count
    removal = 0
    for dict in user_des.destinations:
        print(dict)
        if dict['city']:
            print("filled")
        else:
            removal += 1
            print("empty")
    for step in range(0, removal):
        user_des.destinations.remove({'city': None, 'price_ceiling': None})

    # # This shows all the column names and their corresponding data.
    # print(user_des.__dict__)
    # # Same thing, but keys are in the same order as designated in the table
    # # NOTE: no 'destinations' field
    # destination_dict = dict((col, getattr(user_des, col)) for col in Destinations.__table__.columns.keys())
    # print(destination_dict)

    # Pass in SQLAlchemy Query object to help pre-populate the form with the user's current data
    form = DestinationForm(obj=user_des)

    if form.validate_on_submit():
        # destination entries are dynamic, meaning user chooses how many to enter (between 3 and 10)
        # Since updating a row in SQLAlchemy requires a BaseQuery object, and it is unscriptable,
        # We are unable to loop through the entries and update based on the length.
        # Updates are manually entered with attributes, so since we can't predict how many, we have to update all
        # Below is my very unelegant solution: Create a list of values equal to the total number of columns to update
        # cycle through the entries and replace the default values, then update the list.
        # need a step in the loop ('z') since entry has 2 nested values
        update_list = [None for x in range(0, 20)]
        z = 0
        destinations = form.destinations.entries
        for x in range(0, len(destinations)):
            dest_dict = destinations[x].data
            # This is the submitted data: a dictionary with the city and price
            print(dest_dict)
            update_list[z] = dest_dict['city']
            z += 1
            update_list[z] = dest_dict['price_ceiling']
            z += 1

        # Again, very lengthy since each update must be done manually.
        # All this work so that users can dynamically choose number of destinations AND so when they go to update
        # it will pre-populate the form so they see their older values while updating/editing.
        # Small feature, big headache!

        user_des.home_airport = form.home_airport.data.upper()
        user_des.city1 = update_list[0]
        user_des.price1 = update_list[1]
        user_des.city2 = update_list[2]
        user_des.price2 = update_list[3]
        user_des.city3 = update_list[4]
        user_des.price3 = update_list[5]
        user_des.city4 = update_list[6]
        user_des.price4 = update_list[7]
        user_des.city5 = update_list[8]
        user_des.price5 = update_list[9]
        user_des.city6 = update_list[10]
        user_des.price6 = update_list[11]
        user_des.city7 = update_list[12]
        user_des.price7 = update_list[13]
        user_des.city8 = update_list[14]
        user_des.price8 = update_list[15]
        user_des.city9 = update_list[16]
        user_des.price9 = update_list[17]
        user_des.city10 = update_list[18]
        user_des.price10 = update_list[19]

        db.session.commit()

        flash("Your destinations have been successfully updated.")
        return redirect(url_for('my_destinations'))
    return render_template("update_destinations.html", form=form, page_title=page_title)


@app.route('/my_preferences')
@login_required
def my_preferences():
    page_title = "My Preferences"
    prefs = Preferences.query.filter_by(user_pref_id=current_user.id).first()
    # Turn the query object info into a dictionary with column name: value
    # pref_dict = dict((col, getattr(prefs, col)) for col in Preferences.__table__.columns.keys())
    # print(pref_dict)

    return render_template("my_preferences.html", page_title=page_title, prefs=prefs)


@app.route('/update_preferences', methods=['GET', 'POST'])
@login_required
def update_preferences():
    page_title = "Update Preferences"
    # Grabs the user's current preferences
    prefs = Preferences.query.filter_by(user_pref_id=current_user.id).first()
    # Pass prefs as obj into form: prepopulates the form with the current user's preferences
    form = PreferenceForm(obj=prefs)
    if form.validate_on_submit():

        # POSSIBLE CLEAN SOLUTION TO UPDATING USER PREFERENCES!!
        # form.populate_obj(prefs)
        # ??????????????

        # Now the form data updates the user's preferences.
        # Since form was pre-populated with existing preferences, no bad data or blanks will get updated.
        # Only the things the user wants to change will get changed.
        prefs.email_frequency = form.email_frequency.data
        prefs.min_nights = form.min_nights.data
        prefs.max_nights = form.max_nights.data
        prefs.currency = form.currency.data
        prefs.cabin_class = form.cabin_class.data
        prefs.mix_class = form.mix_class.data
        prefs.exclude_airlines = form.exclude_airlines.data
        prefs.flight_type = form.flight_type.data
        prefs.max_stops = form.max_stops.data
        prefs.max_flight_time = form.max_flight_time.data
        prefs.num_adults = form.num_adults.data
        prefs.num_children = form.num_children.data
        prefs.num_infants = form.num_infants.data
        prefs.search_start_date = form.search_start_date.data
        prefs.specific_search_start_date = form.specific_search_start_date.data
        prefs.search_length = form.search_length.data
        prefs.specific_search_end_date = form.specific_search_end_date.data

        db.session.commit()
        flash("Your preferences have been successfully updated.")
        return redirect(url_for('my_preferences'))
    return render_template("update_preferences.html", form=form, page_title=page_title)


@app.route('/login', methods=["GET", "POST"])
def login():
    page_title = "Login"
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user is None:
            flash(f"Sorry, there is no account for '{email}' in our database.")
            return redirect(url_for('login'))
        if check_password_hash(user.password, password):
            # flash("Login Successful")
            login_user(user)
            return redirect(url_for('user_home'))
        flash("Sorry, the password is incorrect. Please try again.")
        return redirect(url_for('login'))
    return render_template("login.html", form=form, page_title=page_title)


@app.route('/register', methods=['GET', 'POST'])
def register():
    page_title = "Register"
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        if User.query.filter_by(email=email).first():
            flash(f"An account for '{email}' already exists. Please sign in.")
            return redirect(url_for('login'))
        password = form.password.data
        salted_hashbrowns = generate_password_hash(
            password=password,
            method='pbkdf2:sha256',
            salt_length=8
        )

        user = User(email=email,
                    password=salted_hashbrowns,
                    name=form.name.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        preferences = Preferences(
            user_pref=current_user,
            email_frequency=1,
            min_nights=2,
            max_nights=7,
            currency='USD',
            cabin_class='M',
            mix_class='Yes',
            exclude_airlines='Exclude',
            flight_type='round',
            max_stops=3,
            max_flight_time=33,
            num_adults=1,
            num_children=0,
            num_infants=0,
            search_start_date=30,
            search_length=60)
        db.session.add(preferences)
        db.session.commit()

        destinations = Destinations(
            user_dest=current_user,
            home_airport="")
        db.session.add(destinations)
        db.session.commit()
        flash("Account created successfully. Please update your destinations.")
        return redirect(url_for('user_home'))
    return render_template('register.html', form=form, page_title=page_title)


@app.route('/secret')
@admin_only
def secret():
    return render_template('secret.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('logout.html')


login_manager.login_message = ''
login_manager.login_view = 'login'

if __name__ == '__main__':
    app.run()
