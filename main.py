from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import RegisterForm, LoginForm, PreferenceForm, DestinationForm, SendResetEmail, ResetPassword
from functools import wraps
from new_iata_codes import all_cities_international
from numbers_and_letters import COMBINED_LIST
import random
from datetime import date, datetime
# import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'
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
    reset = db.Column(db.String(100))
    reset_timestamp = db.Column(db.String(100))
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
    currency = db.Column(db.String(50))
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
    email = db.Column(db.String(100), nullable=False)
    email_frequency = db.Column(db.Integer)
    email_day = db.Column(db.Integer)
    min_nights = db.Column(db.Integer, nullable=False)
    max_nights = db.Column(db.Integer, nullable=False)
    cabin_class = db.Column(db.String(50), nullable=False)
    exclude_airlines = db.Column(db.String(100), nullable=False)
    max_stops = db.Column(db.Integer)
    max_flight_time = db.Column(db.Integer)
    diff_airports_okay = db.Column(db.String(100))
    num_adults = db.Column(db.Integer, nullable=False)
    num_children = db.Column(db.Integer, nullable=False)
    num_infants = db.Column(db.Integer, nullable=False)
    search_start_date = db.Column(db.Integer)
    specific_search_start_date = db.Column(db.Date)
    search_length = db.Column(db.Integer)
    specific_search_end_date = db.Column(db.Date)


class FlightDeals(db.Model, Base):
    __tablename__ = 'flightdeals'
    id = db.Column(db.Integer, primary_key=True)
    user_deals_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_deals = relationship("User", back_populates="flight_deals")
    flight_search_date = db.Column(db.String(300))
    place1 = db.Column(db.String(300))
    message1 = db.Column(db.String(1000))
    link1 = db.Column(db.String(1000))
    place2 = db.Column(db.String(300))
    message2 = db.Column(db.String(1000))
    link2 = db.Column(db.String(1000))
    place3 = db.Column(db.String(300))
    message3 = db.Column(db.String(1000))
    link3 = db.Column(db.String(1000))
    place4 = db.Column(db.String(300))
    message4 = db.Column(db.String(1000))
    link4 = db.Column(db.String(1000))
    place5 = db.Column(db.String(300))
    message5 = db.Column(db.String(1000))
    link5 = db.Column(db.String(1000))
    place6 = db.Column(db.String(300))
    message6 = db.Column(db.String(1000))
    link6 = db.Column(db.String(1000))
    place7 = db.Column(db.String(300))
    message7 = db.Column(db.String(1000))
    link7 = db.Column(db.String(1000))
    place8 = db.Column(db.String(300))
    message8 = db.Column(db.String(1000))
    link8 = db.Column(db.String(1000))
    place9 = db.Column(db.String(300))
    message9 = db.Column(db.String(1000))
    link9 = db.Column(db.String(1000))
    place10 = db.Column(db.String(300))
    message10 = db.Column(db.String(1000))
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


@app.route('/reset_password_page', methods=["GET","POST"])
def reset_password_page():
    form = SendResetEmail()
    page_title = "Send Password Reset Email"
    if form.validate_on_submit():
        timestamp = datetime.today()
        print(timestamp)
        # Convert into string?
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        print(user)
        if user is None:
            flash(f"Sorry, there is no account for '{email}' in our database.")
            return redirect(url_for('reset_password_page'))

        seq_len = random.randint(70, 90)
        print(seq_len)
        reset_string = ""
        for x in range(0, seq_len):
            reset_string += random.choice(COMBINED_LIST)
        print(reset_string)
        user.reset = reset_string
        user.reset_timestamp = "timestamp"
        db.session.commit()

        # send email to user with a link with string at end

        return render_template("reset_email_sent.html", page_title="Reset Email Sent!")

    return render_template("reset_password.html", page_title=page_title, form=form)


@app.route('/22dneirfymdrowssapruoytogrofuoykosti/<user_recovery_string>', methods=["GET", "POST"])
def authenticate_reset_password(user_recovery_string):

    form = ResetPassword()
    page_title = "Reset Your Password"
    if form.validate_on_submit():
        current_timestamp = datetime.today()
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        print(user)
        if user is None:
            flash(f"Sorry, there is no account for '{email}' in our database.")
            return redirect(url_for('authenticate_reset_password', user_recovery_string=user_recovery_string))
        if user.reset is None:
            flash(f"Sorry, your reset link token has expired, please submit a new reset email request.")
            return redirect(url_for("reset_password_page"))

        # reformat user.reset_timestamp into datetime
        # if current_timestamp - user.reset_timestamp < 30 minutes:
        #     flash(f"Sorry, your reset link token has expired, please submit a new reset email request.")
        #     return redirect(url_for("reset_password_page"))

        if user.reset == user_recovery_string:
            password = form.password.data
            salted_hashbrowns = generate_password_hash(
                password=password,
                method='pbkdf2:sha256',
                salt_length=8
            )
            user.password = salted_hashbrowns
            user.reset = None
            db.session.commit()

            # send email to user noting that they changed their password

            return render_template("reset_password_success.html", page_title="Password Reset Successfully!")
    return render_template("reset_password.html", page_title=page_title, form=form)


@app.route('/home')
@login_required
def user_home():
    user_name = current_user.name
    page_title = f"Hello, {user_name}"
    return render_template("user_home.html", page_title=page_title)

# @app.route('/new', methods=["GET", "POST"])
# def new():
#     cities = all_cities_international
#     form = TrialForm()
#     if form.validate_on_submit():
#         print("Success")
#         print(form.trial.data)
#     return render_template('new_register.html', form=form, cities=cities)

@app.route('/my_deals')
@login_required
def my_deals():
    page_title = "My Flight Deals"
    user_deals = FlightDeals.query.filter_by(user_deals_id=current_user.id).first().__dict__
    print(user_deals)
    return render_template("my_deals.html", page_title=page_title, user_deals=user_deals)




@app.route('/my_destinations')
@login_required
def my_destinations():
    page_title = "My Destinations"
    city_options = all_cities_international
    des = Destinations.query.filter_by(user_dest_id=current_user.id).first().__dict__
    return render_template("my_destinations.html", page_title=page_title, des=des, city_options=city_options)


@app.route('/update_destinations', methods=['GET', 'POST'])
@login_required
def update_destinations():
    page_title = "Update Destinations"
    city_options = all_cities_international
    # Grabs the current user object which contains their data
    user_des = Destinations.query.filter_by(user_dest_id=current_user.id).first()
    # Form obj below doesn't populate fields contained within the FieldList/FormField.
    # instead, need to manually add the data from the user object and pass it as a list of dictionaries
    # to the SQL table variable that matches the name of the FieldList variable in the form (ex: 'destinations)
    user_data_dict = user_des.__dict__
    print(user_data_dict)
    list_of_dicts = []
    for x in range(1, 11):
        if user_data_dict[f'city{x}'] is None:
            pass
        else:
            dict_to_add = {"city": city_options[user_data_dict[f'city{x}']], "price_ceiling": user_data_dict[f'price{x}']}
            list_of_dicts.append(dict_to_add)
    user_des.destinations = list_of_dicts
    user_des.home_airport = city_options[user_data_dict["home_airport"]]
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

        home_airport = [iata_code for iata_code, home in city_options.items() if home == form.home_airport.data][0]
        print(f"Home Airport: {home_airport}")
        update_list = [None for x in range(0, 20)]
        z = 0
        destinations = form.destinations.entries
        for x in range(0, len(destinations)):
            dest_dict = destinations[x].data
            # This is the submitted data: a dictionary with the city and price
            print(dest_dict)

            update_list[z] = [iata_code for iata_code, city_name in city_options.items() if city_name == dest_dict['city']][0]
            z += 1
            update_list[z] = dest_dict['price_ceiling']
            z += 1

        # Again, very lengthy since each update must be done manually.
        # All this work so that users can dynamically choose number of destinations AND so when they go to update
        # it will pre-populate the form so they see their older values while updating/editing.
        # Small feature, big headache!

        user_des.home_airport = home_airport
        user_des.currency = form.currency.data
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
    return render_template("update_destinations.html", form=form, page_title=page_title, city_options=city_options)


@app.route('/my_preferences')
@login_required
def my_preferences():
    page_title = "My Preferences"
    prefs = Preferences.query.filter_by(user_pref_id=current_user.id).first()

    email_freq_dict = {1: "Once a week", 2: "Once every two weeks", 3: "Once every two weeks",
                       4: "Once a month", 5: "Once a month", 6: "Once a month", 7: "Once a month"}
    email_day_dict = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
    cabin_class_dict = {'M': 'Economy', 'W': 'Premium Economy', 'C': 'Business', 'F': 'First Class'}
    exclude_airlines_dict = {'true': 'Exclude Lowest Rated Airlines', 'false': 'Include All Airlines'}
    lead_time_dict = {1: 'One day', 7: 'One week', 14: 'Two weeks', 21: 'Three weeks', 30: 'One month',
                      60: 'Two months', 90: 'Three months', 0: 'Using Specific Date'}
    search_length_dict = {7: 'One week', 14: 'Two weeks', 21: 'Three weeks', 30: 'One month',
                          60: 'Two months', 90: 'Three months', 120: 'Four months', 150: 'Five months',
                          180: 'Six months', 0: 'Using Specific Date'}
    start_specific = None
    end_specific = None
    if prefs.specific_search_start_date:
        start_specific = prefs.specific_search_start_date.strftime('%a, %B %-d')
    if prefs.specific_search_end_date:
        end_specific = prefs.specific_search_end_date.strftime('%a, %B %-d')

    preferences_dictionary = {"email_freq": email_freq_dict, "email_day": email_day_dict,
                              "cabin_class": cabin_class_dict, "exclude_airlines": exclude_airlines_dict,
                              "lead_time_start": lead_time_dict, "search_length": search_length_dict,
                              "start_specific": start_specific, "end_specific": end_specific}

    return render_template("my_preferences.html", page_title=page_title, prefs=prefs, pref_dict=preferences_dictionary)


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
        prefs.email = form.email.data
        prefs.email_frequency = form.email_frequency.data
        prefs.email_day = form.email_day.data
        prefs.min_nights = form.min_nights.data
        prefs.max_nights = form.max_nights.data
        prefs.cabin_class = form.cabin_class.data
        prefs.exclude_airlines = form.exclude_airlines.data
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
                    reset=None,
                    name=form.name.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        preferences = Preferences(
            user_pref=current_user,
            email=user.email,
            email_frequency=1,
            email_day=4,
            min_nights=2,
            max_nights=7,
            cabin_class='M',
            exclude_airlines='True',
            max_stops=2,
            max_flight_time=35,
            diff_airports_okay="True",
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

        flight_deals = FlightDeals(
            user_deals=current_user)
        db.session.add(flight_deals)
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
