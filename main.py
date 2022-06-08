from flask import Flask, render_template, redirect, url_for, flash, abort, request, session
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import RegisterForm, LoginForm, PreferenceForm, DestinationForm, SendResetEmail, \
                    ResetPassword, SubmitTicketForm, ChangeEmailForm, ChangePasswordForm
from functools import wraps
from new_iata_codes import all_cities_international
from numbers_and_letters import COMBINED_LIST
import random
import requests
import ast
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'
api_key = "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"
company_email = "flightclubdeals@gmail.com"
company_name = "Flight Club"
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
    join_type = db.Column(db.String(50))
    confirmation_token = db.Column(db.String(300))
    confirmed = db.Column(db.Boolean)
    reset_token = db.Column(db.String(100))
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


def send_email(company_email, company_name, user_name, user_email, subject, params: dict, template_id, api_key):
    url = "https://api.sendinblue.com/v3/smtp/email"
    payload = {
        "sender": {
            "email": company_email,
            "name": company_name
        },
        "to": [{
            "email": user_email,
            "name": user_name
        }],
        "subject": subject,
        "params": params,
        "templateId": template_id
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "api-key": api_key
    }
    response = requests.post(url, json=payload, headers=headers)
    print(response.text)
    return response.text


def create_random_string():
    seq_len = random.randint(75, 97)
    print(seq_len)
    random_string = ""
    for x in range(0, seq_len):
        random_string += random.choice(COMBINED_LIST)
    print(random_string)
    return random_string


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
    return User.query.get(user_id)


@app.route('/')
def landing_page():
    return render_template("index.html", page_title="")


@app.route('/redirect/<params>/<page_title>/<action>')
def action_successful_redirect(params, page_title, action):
    parameters = ast.literal_eval(params)
    session['params'] = parameters
    session['page_title'] = page_title
    return redirect(url_for('action_success', action=action))


@app.route('/<action>')
def action_success(action):
    params = session.get('params', None)
    page_title = session.get('page_title', None)
    return render_template("action_successful.html", params=params, page_title=page_title)


@app.route('/confirm_your_account/<confirm_string>', methods=["GET"])
def confirm_your_account(confirm_string):
    print(f"confirm string: {confirm_string}")
    page_title = "Confirm Your Account"
    params = {"heading": "Your account has been confirmed!",
              "body1": "You've climbed the ladder, said the secret password, "
                       "and the wooden door has opened for you.",
              "body2": "Welcome to the club, my friend!",
              "button_text": "Go to My Account",
              "url_for": "user_home"}
    all_users = User.query.all()
    for user in all_users:

        if user.confirmed:
            if user.confirmation_token == confirm_string:
                return redirect(url_for('action_successful_redirect', params=params, page_title="Account Confirmed!",
                                        action="confirmation_success"))
                # return render_template("action_successful.html", params=params, page_title="Account Confirmed!")
            else:
                continue
        # Since tokens are unique, we can confirm without checking which user is confirming
        elif user.confirmation_token == confirm_string:
            user.confirmed = True
            db.session.commit()

            login_user(user)
            return redirect(url_for('action_successful_redirect', params=params, page_title="Account Confirmed!",
                                    action="confirmation_success"))
            # return render_template("action_successful.html", params=params, page_title="Account Confirmed!")
        else:
            continue

    return render_template("confirm_your_account.html", page_title=page_title)


@app.route('/reset_your_password', methods=["GET", "POST"])
def reset_your_password():
    form = SendResetEmail()
    page_title = "Reset Your Password"
    if form.validate_on_submit():
        timestamp = datetime.today()
        print(timestamp)
        # Convert into string?
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        print(user)
        if user is None:
            flash(f"Sorry, there is no account for '{email}' in our database.")
            return redirect(url_for('reset_your_password'))

        reset_string = create_random_string()

        user.reset_token = reset_string
        user.reset_timestamp = timestamp
        db.session.commit()

        # send email to user with a link with string at end
        subject = "Password Reset Request"
        email_params = {"reset_token": reset_string, "notify": "notify_link_ADD LATER"}
        template_id = 4
        email_status = send_email(company_email=company_email,
                                  company_name=company_name,
                                  user_name=user.name,
                                  user_email=user.email,
                                  subject=subject,
                                  params=email_params,
                                  template_id=template_id,
                                  api_key=api_key)

        if email_status == "good":
            pass

        params = {"heading": "An email has been sent to help you reset your password.",
                  "body1": "Please check your email and follow the instructions provided.",
                  "body2": None,
                  "button_text": None,
                  "url_for": None}
        return redirect(url_for('action_successful_redirect', params=params, page_title="Reset Email Sent!",
                                action="reset_email_sent"))
        # return render_template("action_successful.html", page_title="Reset Email Sent!", params=params)

    return render_template("send_reset_email.html", page_title=page_title, form=form)


@app.route('/itsokfriendweforgiveyou/<user_recovery_string>', methods=["GET", "POST"])
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

        if user.reset_token is None:
            flash(f"Sorry, your reset link token has expired, please submit a new reset email request.")
            return redirect(url_for("reset_your_password"))

        print(user.reset_timestamp)
        print(type(user.reset_timestamp))
        # reformat user.reset_timestamp into datetime
        timestamp_config = tuple([int(x) for x in user.reset_timestamp[:10].split('-')]) + \
                           tuple([int(float(x)) for x in user.reset_timestamp[11:].split(':')])
        print(timestamp_config)
        reset_timestamp = datetime(*timestamp_config)

        print(reset_timestamp)
        print(current_timestamp)
        td = current_timestamp - reset_timestamp
        print(td)
        time_difference_mins = int(round(td.total_seconds() / 60))
        print(time_difference_mins)

        if time_difference_mins > 30:
            user.reset_token = None
            flash(f"Sorry, your reset link token has expired, please submit a new reset email request.")
            return redirect(url_for("reset_your_password"))

        if user.reset_token == user_recovery_string:
            password = form.password.data
            salted_hashbrowns = generate_password_hash(
                password=password,
                method='pbkdf2:sha256',
                salt_length=8
            )
            user.password = salted_hashbrowns
            user.reset_token = None
            db.session.commit()

            # send email to user noting that they changed their password

            params = {"heading": "Your password has been reset to your new password",
                      "body1": "Please login to your account.",
                      "body2": None,
                      "button_text": "Go to Login Page",
                      "url_for": 'login'}

            return redirect(url_for('action_successful_redirect', params=params, page_title="Password Reset Successfully!",
                                    action="password_reset_success"))
            # return render_template("action_successful.html", params=params, page_title="Password Reset Successfully!")

        return redirect(url_for('landing_page'))

    return render_template("reset_password.html", page_title=page_title, form=form)


@app.route('/submit_ticket', methods=["GET", "POST"])
@login_required
def submit_ticket():
    page_title = "Have A Concern?"
    form = SubmitTicketForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=current_user.id).first()
        print(user.email)
        # send email to user as a copy of their ticket
        # send email to FlightClub to notify of a ticket submission
        print("Success")

        params = {"heading": "Your issue has been successfully reported",
                  "body1": "An email has been sent to Flight Club about your concern. "
                           "You have also been sent an email with the details of your report.",
                  "body2": "Flight Club will try to respond to this concern in a timely manner."
                           "Thank you for your patience",
                  "button_text": "Return to Home",
                  "url_for": 'user_home'}
        return redirect(url_for('action_successful_redirect', params=params, page_title="Report Submitted!",
                                action="report_submitted"))
        # return render_template('action_successful.html', params=params, page_title="Report Submitted!")

    return render_template('submit_ticket.html', form=form, page_title=page_title)


@app.route('/home')
@login_required
def user_home():
    user_name = current_user.name
    page_title = f"Hello, {user_name}"
    return render_template("user_home.html", page_title=page_title)


@app.route('/my_account')
@login_required
def my_account():
    page_title = "My Account"
    return render_template("my_account.html", page_title=page_title)


@app.route('/my_account/change_email', methods=["GET", "POST"])
@login_required
def change_email():
    page_title = "Change Your Email"
    form = ChangeEmailForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=current_user.id).first()
        current_password = form.password.data
        if User.query.filter_by(email=form.email.data).first():
            flash(f"An account for '{form.email.data}' already exists. Please try a different email address")
            return redirect(url_for('change_email'))
        if check_password_hash(user.password, current_password):
            all_users = User.query.all()
            confirmation_string = create_random_string()
            # check existing tokens, makes sure no one has the same token (even though the odds are insanely small)
            all_confirmations_tokens = [user.confirmation_token for user in all_users]
            while confirmation_string in all_confirmations_tokens:
                confirmation_string = create_random_string()
            user.email = form.email.data
            user.confirmation_token = confirmation_string
            user.confirmed = False
            db.session.commit()
            logout_user()
            # email_params = {"confirmation_token": confirmation_string, "name": user.name}
            # send_email(company_email=company_email, company_name=company_name,
            #            user_name=user.name, user_email=user.email,
            #            subject="Account Confirmation", params=email_params,
            #            template_id=5, api_key=api_key)

            params = {"heading": "Please check your email to confirm your change of email address",
                      "body1": "Again, if you don't see an email from us in your inbox, check your spam folder.",
                      "body2": "And if it unfortunately landed in the spam folder, make sure to mark it as 'Not Spam' "
                               "so that our other emails (and your deals!) don't get sent there as well.",
                      "button_text": None,
                      "url_for": None}

            return redirect(url_for('action_successful_redirect', params=params, page_title="Confirm Your New Email",
                                    action="confirmation_email_sent"))
        else:
            flash("Sorry, your current password was incorrect.")
            return redirect(url_for('change_email'))
    return render_template("change_email.html", page_title=page_title, form=form)


@app.route('/my_account/change_password', methods=["GET", "POST"])
@login_required
def change_password():
    page_title = "Change Your Password"
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=current_user.id).first()
        current_password = form.password.data
        if check_password_hash(user.password, current_password):
            new_password = form.new_password.data
            salted_hashbrowns = generate_password_hash(
                password=new_password,
                method='pbkdf2:sha256',
                salt_length=8
            )
            user.password = salted_hashbrowns
            db.session.commit()
            params = {"heading": "Your password has been successfully changed",
                      "body1": "Please login to your account again.",
                      "body2": None,
                      "button_text": "Go to Login Page",
                      "url_for": 'login'}

            return redirect(
                url_for('action_successful_redirect', params=params, page_title="Password Changed Successfully!",
                        action="change_password_success"))
        else:
            flash("Sorry, your current password was incorrect.")
            return redirect(url_for('change_password'))
    return render_template("change_password.html", page_title=page_title, form=form)


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
            dict_to_add = {"city": city_options[user_data_dict[f'city{x}']],
                           "price_ceiling": user_data_dict[f'price{x}']}
            list_of_dicts.append(dict_to_add)
    user_des.destinations = list_of_dicts
    if user_des.home_airport is None:
        pass
    else:
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

        destinations_update_dict = {"home_airport": home_airport, "currency": form.currency.data}

        for x in range(1, 11):
            destinations_update_dict[f"city{x}"] = None
            destinations_update_dict[f"price{x}"] = None

        destinations = form.destinations.entries
        for x in range(0, len(destinations)):
            dest_dict = destinations[x].data
            destinations_update_dict[f"city{x + 1}"] = [iata_code for iata_code, city_name in city_options.items()
                                                    if city_name == dest_dict['city']][0]
            destinations_update_dict[f"price{x + 1}"] = dest_dict['price_ceiling']

        Destinations.query.filter_by(user_dest_id=current_user.id).update(destinations_update_dict)

        db.session.commit()


        # Again, very lengthy since each update must be done manually.
        # All this work so that users can dynamically choose number of destinations AND so when they go to update
        # it will pre-populate the form so they see their older values while updating/editing.
        # Small feature, big headache!

        # user_des.home_airport = home_airport
        # user_des.currency = form.currency.data
        # user_des.city1 = update_list[0]
        # user_des.price1 = update_list[1]
        # user_des.city2 = update_list[2]
        # user_des.price2 = update_list[3]
        # user_des.city3 = update_list[4]
        # user_des.price3 = update_list[5]
        # user_des.city4 = update_list[6]
        # user_des.price4 = update_list[7]
        # user_des.city5 = update_list[8]
        # user_des.price5 = update_list[9]
        # user_des.city6 = update_list[10]
        # user_des.price6 = update_list[11]
        # user_des.city7 = update_list[12]
        # user_des.price7 = update_list[13]
        # user_des.city8 = update_list[14]
        # user_des.price8 = update_list[15]
        # user_des.city9 = update_list[16]
        # user_des.price9 = update_list[17]
        # user_des.city10 = update_list[18]
        # user_des.price10 = update_list[19]

        # db.session.commit()

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
    exclude_airlines_dict = {'true': 'Exclude Lowest Rated', 'false': 'Include All Airlines'}
    lead_time_dict = {1: 'One day', 7: 'One week', 14: 'Two weeks', 21: 'Three weeks', 30: 'One month',
                      60: 'Two months', 90: 'Three months', 0: 'Using Specific Date'}
    search_length_dict = {7: 'One week', 14: 'Two weeks', 21: 'Three weeks', 30: 'One month',
                          60: 'Two months', 90: 'Three months', 120: 'Four months', 150: 'Five months',
                          180: 'Six months', 0: 'Using Specific Date'}
    start_specific = None
    end_specific = None
    if prefs.specific_search_start_date:
        start_specific = prefs.specific_search_start_date.strftime('%a, %B %-d, %Y')
    if prefs.specific_search_end_date:
        end_specific = prefs.specific_search_end_date.strftime('%a, %B %-d, %Y')

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
    # Pass prefs as obj into form: populates the form with the current user's preferences
    print(prefs.email_frequency)
    # helps solve gap in user choices and back-end functionality method (flight_search.py changes their db value)
    if prefs.email_frequency == 3:
        prefs.email_frequency = 2
    if prefs.email_frequency in (5, 6, 7):
        prefs.email_frequency = 4

    print(prefs.email_frequency)
    form = PreferenceForm(obj=prefs)
    if form.validate_on_submit():

        # POSSIBLE CLEAN SOLUTION TO UPDATING USER PREFERENCES!!
        # form.populate_obj(prefs)
        # ??????????????
        # Now the form data updates the user's preferences.
        # Since form was pre-populated with existing preferences, no bad data or blanks will get updated.
        # Only the things the user wants to change will get changed.

        updated_preferences = {
            "email": form.email.data, "email_frequency": form.email_frequency.data, "email_day": form.email_day.data,
            "min_nights": form.min_nights.data, "max_nights": form.max_nights.data,
            "cabin_class": form.cabin_class.data, "exclude_airlines": form.exclude_airlines.data,
            "max_stops": form.max_stops.data, "max_flight_time": form.max_flight_time.data,
            "num_adults": form.num_adults.data, "num_children": form.num_children.data,
            "num_infants": form.num_infants.data, "search_start_date": form.search_start_date.data,
            "specific_search_start_date": form.specific_search_start_date.data,
            "search_length": form.search_length.data, "specific_search_end_date": form.specific_search_end_date.data
        }

        Preferences.query.filter_by(user_pref_id=current_user.id).update(updated_preferences)

        db.session.commit()

        # prefs.email = form.email.data
        # prefs.email_frequency = form.email_frequency.data
        # prefs.email_day = form.email_day.data
        # prefs.min_nights = form.min_nights.data
        # prefs.max_nights = form.max_nights.data
        # prefs.cabin_class = form.cabin_class.data
        # prefs.exclude_airlines = form.exclude_airlines.data
        # prefs.max_stops = form.max_stops.data
        # prefs.max_flight_time = form.max_flight_time.data
        # prefs.num_adults = form.num_adults.data
        # prefs.num_children = form.num_children.data
        # prefs.num_infants = form.num_infants.data
        # prefs.search_start_date = form.search_start_date.data
        # prefs.specific_search_start_date = form.specific_search_start_date.data
        # prefs.search_length = form.search_length.data
        # prefs.specific_search_end_date = form.specific_search_end_date.data


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
        if not user.confirmed:
            return render_template("confirm_your_account.html", page_title="Confirm Your Account")
        if check_password_hash(user.password, password):
            # flash("Login Successful")
            login_user(user)
            return redirect(url_for('user_home'))

        # Prepopulate email field so user doesn't need to retype it???

        flash("Sorry, the password is incorrect. Please try again.")
        return redirect(url_for('login'))
    return render_template("login.html", form=form, page_title=page_title)


@app.route('/create_an_account/<join_type>', methods=['GET', 'POST'])
def create_an_account(join_type):
    page_title = "Create an Account"
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
        all_users = User.query.all()
        confirmation_string = create_random_string()
        # check existing tokens, makes sure no one has the same token (even though the odds are insanely small)
        all_confirmations_tokens = [user.confirmation_token for user in all_users]
        while confirmation_string in all_confirmations_tokens:
            confirmation_string = create_random_string()

        user = User(email=email,
                    password=salted_hashbrowns,
                    join_type=join_type,
                    confirmed=False,
                    confirmation_token=confirmation_string,
                    name=form.name.data)
        db.session.add(user)
        db.session.commit()

        # params = {"confirmation_token": confirmation_string, "name": user.name}
        # send_email(company_email=company_email, company_name=company_name,
        #            user_name=user.name, user_email=user.email,
        #            subject="Account Confirmation", params=params,
        #            template_id=5, api_key=api_key)

        preferences = Preferences(
            user_pref=user,
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

        destinations = Destinations(user_dest=user)
        db.session.add(destinations)
        db.session.commit()

        flight_deals = FlightDeals(user_deals=user)
        db.session.add(flight_deals)
        db.session.commit()

        params = {"heading": "Please check your email to confirm your account",
                  "body1": "If you don't see an email from us in your inbox, check your spam folder.",
                  "body2": "If it unfortunately landed in the spam folder, make sure to mark it as 'Not Spam' "
                           "so that our other emails (and your deals!) don't get sent there as well.",
                  "button_text": None,
                  "url_for": None}

        return redirect(url_for('action_successful_redirect', params=params, page_title="Almost there...",
                                action="confirmation_email_sent"))
        # return render_template("confirm_your_account.html", page_title=page_title)
    return render_template('register.html', form=form, page_title=page_title)


@app.route('/secret')
@admin_only
def secret():
    # Placeholder location for now
    # Will add admin features according to the needs of the projects (once users become active and problems arise)
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
