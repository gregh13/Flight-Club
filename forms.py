from flask import flash
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from datetime import timedelta, date
from new_iata_codes import all_cities_international

city_list = [all_cities_international[iata] for iata in all_cities_international]


def invalid_date(form, field):
    if field.data < date.today():
        flash("Error: You can't choose a specific date that is in the past! Only future dates are accepted",
              "error")
        raise ValidationError()


def date_range_check(form, field):
    if form.specific_search_start_date.data:
        if field.data < form.specific_search_start_date.data:
            flash("*** Error: You can't choose a specific End Date that's "
                  "earlier than your specific Start Date. ***", "error")
            raise ValidationError()
        if field.data < (form.specific_search_start_date.data + timedelta(days=form.min_nights.data)):
            flash("*** Error: You can't have a specific date range that is "
                  "shorter than your minimum nights setting. ***", "error")
            raise ValidationError()


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


class ChangeEmailForm(FlaskForm):
    email = EmailField("New Email Address", validators=[InputRequired()])
    confirm_email = EmailField("Confirm New Email", validators=[InputRequired(),
                                                                EqualTo('email', message='Emails must match')])
    password = PasswordField("Current Password", validators=[InputRequired()])
    submit = SubmitField("Send Confirmation Email")


class ChangePasswordForm(FlaskForm):
    password = PasswordField("Current Password", validators=[InputRequired(), Length(min=8, max=22)])
    new_password = PasswordField("New Password", validators=[InputRequired(), Length(min=8, max=22)])
    confirm_password = PasswordField("Confirm New Password",
                                     validators=[InputRequired(),
                                                 Length(min=8, max=22),
                                                 EqualTo('new_password', message='Passwords must match')])
    submit = SubmitField("Change Password")


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
    email_frequency = SelectField("Email Frequency", choices=[(1, "Once a week"), (2, "Once every two weeks"),
                                                              (4, "Once a month")], validators=[InputRequired()])
    email_day = SelectField("Day of Week to Receive Email",
                            choices=[(0, "Monday"), (1, "Tuesday"), (2, "Wednesday"), (3, "Thursday"),
                                     (4, "Friday"), (5, "Saturday"), (6, "Sunday")])

    cabin_class = SelectField("Cabin Class", choices=[('M', 'Economy'), ('W', 'Premium Economy'),
                                                      ('C', 'Business'), ('F', 'First Class')], validators=[Optional()])
    exclude_airlines = SelectField("Exclude Lowest Rated Airlines?",
                                   choices=[("", "Select Option"), ('true', 'Exclude Lowest Rated Airlines'),
                                            ('false', 'Include All Airlines')],
                                   validators=[Optional()],
                                   description="Excludes airlines rated lowest in safety, service, claims processing, "
                                               "and punctuality from your flight search (e.g. Ryan Air, EasyJet, "
                                               "Lion Air, China Eastern, Spirit, etc.)")
    max_stops = IntegerField("Max Number of Stops (One Way)", validators=[Optional(), NumberRange(min=0)])
    max_flight_time = IntegerField("Max Flight Duration", validators=[Optional(), NumberRange(min=1)])
    num_adults = IntegerField("Adults", validators=[InputRequired(), NumberRange(min=1, max=6)])
    num_children = IntegerField("Children (Age 2-11)", validators=[InputRequired(), NumberRange(min=0, max=4)])
    num_infants = IntegerField("Infants (Age < 2)", validators=[InputRequired(), NumberRange(min=0, max=3)])
    min_nights = IntegerField("Trip Duration: Min Nights", validators=[InputRequired(), NumberRange(min=0)],
                              description="The minimum possible length of time spent at your travel destination. "
                                          "Actual trip duration might be somewhere in-between the min and max nights")
    max_nights = IntegerField("Trip Duration: Max Nights", validators=[InputRequired(), NumberRange(min=0)],
                              description="The maximum possible length of time spent at your travel destination. "
                                          "Actual trip duration might be somewhere in-between the min and max nights")
    search_start_date = SelectField("Lead Time for Search", coerce=int,
                                    choices=[(1, 'One day'), (7, 'One week'),
                                             (14, 'Two weeks'), (21, 'Three weeks'), (30, 'One month'),
                                             (60, 'Two months'), (90, 'Three months')],
                                    validators=[InputRequired()],
                                    description="This is a rolling date, meaning it will move as time passes. "
                                                "For example: If you choose 'two weeks', then if the flight search "
                                                "occurs on March 10th, it will look for flights starting from "
                                                "March 24th onwards.")
    search_length = SelectField("Time Window for Search", coerce=int,
                                choices=[(14, 'Two weeks'), (21, 'Three weeks'), (30, 'One month'),
                                         (60, 'Two months'), (90, 'Three months'), (120, 'Four months'),
                                         (150, 'Five months'), (180, 'Six months')],
                                validators=[InputRequired()],
                                description="This is a rolling date range, meaning it will move as time passes. "
                                            "For example, if you have a lead time of  '1 month'  and a time window of "
                                            "'3 months' , then if it searches on September 10th, it would look for all "
                                            "flights from October 10th to January 10th.")
    specific_search_start_date = DateField('Specific Start Date', validators=[Optional(), invalid_date],
                                           description="This is a fixed date which will not move as time passes. "
                                                       "Choose this if you have a specific date range available to "
                                                       "travel (holidays, summer vacation, etc.), "
                                                       "otherwise leave blank.")
    specific_search_end_date = DateField('Specific End Date',
                                         validators=[Optional(), invalid_date, date_range_check],
                                         description="This is a fixed date which will not move as time passes. "
                                                     "Choose this if you have a specific date range available to "
                                                     "travel (holidays, summer vacation, etc.), otherwise leave blank.")
    submit = SubmitField("Save Changes")
