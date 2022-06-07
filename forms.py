from flask import flash
from flask_wtf import FlaskForm, Form
from wtforms import *
from wtforms.validators import *
from datetime import timedelta, date
from new_iata_codes import all_cities_international

city_list = [all_cities_international[iata] for iata in all_cities_international]


def invalid_date(form, field):
    if field.data < date.today():
        flash("Error: You can't choose a specific date that is in the past! Only future dates are accepted",
              "error")
        raise ValidationError(
            "Note: This is a fixed date which will not move as time passes. Choose this if you only have specific date ranges available to travel (holidays, summer, etc.)")


def date_range_check(form, field):
    if form.specific_search_start_date.data:
        if field.data < form.specific_search_start_date.data:
            flash("*** Error: You can't choose a specific End Date that's earlier than your specific Start Date. ***", "error")
            raise ValidationError("Note: This is a fixed date which will not move as time passes. Choose this if you only have specific date ranges available to travel (holidays, summer, etc.)")
        if field.data < (form.specific_search_start_date.data + timedelta(days=(form.min_nights.data))):
            flash("*** Error: You can't have a specific date range that is shorter than your minimum nights setting. ***", "error")
            raise ValidationError("Note: This is a fixed date which will not move as time passes. Choose this if you only have specific date ranges available to travel (holidays, summer, etc.)")


# # WTForm
class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=22)])
    confirm_password = PasswordField("Confirm Password",
                                     validators=[InputRequired(),
                                                 Length(min=8, max=22),
                                                 EqualTo('password', message='Passwords must match')])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")


class SendResetEmail(FlaskForm):
    email = EmailField("Email Address", validators=[InputRequired()])
    submit = SubmitField("Send Reset Email")


class ResetPassword(FlaskForm):
    email = EmailField("Your Email", validators=[InputRequired()])
    password = PasswordField("New Password", validators=[InputRequired(), Length(min=8, max=22)])
    confirm_password = PasswordField("Confirm Password",
                                     validators=[InputRequired(),
                                                 Length(min=8, max=22),
                                                 EqualTo('password', message='Passwords must match')])
    submit = SubmitField("Send Reset Email")


class SubmitTicketForm(FlaskForm):
    issue_subject = StringField("Subject of Issue", validators=[InputRequired()])
    issue_description = TextAreaField("Description of Issue", validators=[InputRequired()])
    submit = SubmitField("Submit")


class CityPriceForm(Form):
    city = StringField("City Name",
                       validators=[InputRequired(),
                                   AnyOf(values=city_list,
                                         message="Please select one of the choices shown as you type.")])

    price_ceiling = IntegerField("Price Ceiling", validators=[InputRequired(), NumberRange(min=1)])


class DestinationForm(FlaskForm):
    search = SearchField("Search field")
    home_airport = StringField("Home Airport", validators=[InputRequired(),
                                                           AnyOf(values=city_list,
                                                                 message="Please select one of the "
                                                                         "choices shown as you type.")])

    currency = SelectField("Currency", choices=['USD', 'EUR', 'SGD', 'AUD', 'THB', 'CNY', 'HUF', 'GBP', 'CAD'],
                           validators=[InputRequired()])
    destinations = FieldList(FormField(CityPriceForm), min_entries=3, max_entries=10)


class PreferenceForm(FlaskForm):
    email = EmailField("Email", validators=[InputRequired()])
    email_frequency = SelectField("Email Frequency", choices=[(1, "Once a week"), (2, "Once every two weeks"), (4, "Once a month")], validators=[InputRequired()])
    email_day = SelectField("Day of Week to Receive Email",
                            choices=[(0, "Monday"), (1, "Tuesday"), (2, "Wednesday"), (3, "Thursday"), (4, "Friday"), (5, "Saturday"), (6, "Sunday")])
    min_nights = IntegerField("Trip Duration: Minimum Number of Nights", validators=[InputRequired(), NumberRange(min=0)], description="The minimum length of time spent at your travel destination.")
    max_nights = IntegerField("Trip Duration: Max Number of Nights", validators=[InputRequired(), NumberRange(min=0)], description="The maximum length of time spent at your travel destination. Actual trip duration will be somewhere in-between the min and max duration")
    cabin_class = SelectField("Cabin Class", choices=[('M', 'Economy'), ('W', 'Premium Economy'), ('C', 'Business'), ('F', 'First Class')], validators=[Optional()])
    exclude_airlines = SelectField("Exclude Lowest Rated Airlines?", choices=[("", "Select Option"), ('true', 'Exclude Lowest Rated Airlines'), ('false', 'Include All Airlines')], validators=[Optional()], description="Excludes airlines rated lowest in safety, service, claims processing, and punctuality from your flight search (e.g. Ryan Air, EasyJet, Lion Air, China Eastern, Spirit, etc.)")
    max_stops = IntegerField("Max Number of Stops (One Way)", validators=[Optional(), NumberRange(min=0)])
    max_flight_time = IntegerField("Max Flight Duration", validators=[Optional(), NumberRange(min=1)])
    num_adults = IntegerField("Number of Adult Passengers", validators=[InputRequired(), NumberRange(min=1, max=6)])
    num_children = IntegerField("Number of Child Passengers (Age 2-11)", validators=[InputRequired(), NumberRange(min=0, max=4)])
    num_infants = IntegerField("Number of Infant Passengers (Age < 2)", validators=[InputRequired(), NumberRange(min=0, max=3)])
    search_start_date = SelectField("How far out should the flight search begin looking for flights", coerce=int,
                                    choices=[(1, 'One day'), (7, 'One week'),
                                             (14, 'Two weeks'), (21, 'Three weeks'), (30, 'One month'),
                                             (60, 'Two months'), (90, 'Three months')],
                                    validators=[InputRequired()], description="Note: This is a rolling date range, meaning it will move as time passes. Since Flight Club searches flights weekly, this is better than a specific date range.")
    specific_search_start_date = DateField('Specific Start Date (Optional)', validators=[Optional(), invalid_date],
                                           description="Note: This is a fixed date which will not move as time passes. Choose this if you only have specific date ranges available to travel (holidays, summer, etc.)")
    search_length = SelectField("Search Date Range (the window of time flights will be searched)", coerce=int,
                                choices=[(14, 'Two weeks'), (21, 'Three weeks'), (30, 'One month'),
                                         (60, 'Two months'), (90, 'Three months'), (120, 'Four months'),
                                         (150, 'Five months'), (180, 'Six months')],
                                validators=[InputRequired()],
                                description="Note: This is also a rolling date range, meaning it will move as time passes. For example, if it begins looking for flights 'One month' out and has a date range of '3 months', then if it searches on June 10th, it would look for all flights between July 10th and October 10th.")
    specific_search_end_date = DateField('Specific End Date (Optional)',
                                           validators=[Optional(), invalid_date, date_range_check], description="Note: This is a fixed date which will not move as time passes. Choose this if you only have specific date ranges available to travel (holidays, summer, etc.)")
    submit = SubmitField("Save Changes")

