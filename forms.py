from flask import flash
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from datetime import timedelta, date
from new_iata_codes import all_cities_international

city_list = [all_cities_international[iata] for iata in all_cities_international]


def invalid_max_nights(form, field):
    if field.data < form.min_nights.data:
        # flash("Max number of nights can't be less than your minimum number of nights.")
        raise ValidationError("Max number of nights can't be less than your minimum number of nights.", "error")


def invalid_date(form, field):
    if field.data < date.today():
        # flash("You can't choose a specific date that is in the past! Only future dates are accepted",

        raise ValidationError(f"You can't choose a {field.label.text} that is in the past! "
                              "Only future dates are accepted","error")


def date_range_check(form, field):
    if form.specific_search_start_date.data:
        if field.data < form.specific_search_start_date.data:
            # flash("You can't choose a specific End Date that's "
            #       "earlier than your specific Start Date.", "error")
            raise ValidationError("You can't choose a Specific End Date that's "
                  "earlier than your Specific Start Date.", "error")
        if field.data < (form.specific_search_start_date.data + timedelta(days=form.min_nights.data)):
            # flash("You can't have a specific date range that is "
            #       "shorter than your minimum nights setting.", "error")
            raise ValidationError("You can't have a specific date range that is "
                  "shorter than your minimum nights setting.", "error")


# # WTForm
class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired(message="'Name' field is required")])
    email = EmailField("Email", validators=[InputRequired(message="'Email' field is required"), Email(granular_message=True, check_deliverability=True)])
    password = PasswordField("Password", validators=[InputRequired(message="'Password' field is required"),
                                                     Length(min=8, max=22, message="Password must be between 8 "
                                                                                   "and 22 characters")])
    confirm_password = PasswordField("Confirm Password",
                                     validators=[InputRequired(message="'Confirm Password' field is required"),
                                                 Length(min=8, max=22, message="Password must be between 8 "
                                                                               "and 22 characters"),
                                                 EqualTo('password', message='The passwords must match exactly')])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[InputRequired(message="'Email' field is required"), Email(granular_message=True)])
    password = PasswordField("Password", validators=[InputRequired(message="'Password' field is required")])
    submit = SubmitField("Login")


class ChangeEmailForm(FlaskForm):
    email = EmailField("New Email Address", validators=[InputRequired(message="'New Email Address' field is required"), Email(granular_message=True,
                                                                               check_deliverability=True)])
    confirm_email = EmailField("Confirm New Email", validators=[InputRequired(message="'Confirm New Email' field is required"),
                                                                EqualTo('email', message='The email addresses must match exactly')])
    password = PasswordField("Current Password", validators=[InputRequired(message="'Current Password' field is required")])
    submit = SubmitField("Send Confirmation Email")


class ChangePasswordForm(FlaskForm):
    password = PasswordField("Current Password", validators=[InputRequired(message="'Current Password' field is required")])
    new_password = PasswordField("New Password", validators=[InputRequired(message="'New Password' field is required"),
                                                             Length(min=8, max=22, message="Password must be between 8 "
                                                                                           "and 22 characters")])
    confirm_password = PasswordField("Confirm New Password",
                                     validators=[InputRequired(message="'Confirm New Password' field is required"),
                                                 Length(min=8, max=22, message="Password must be between 8 "
                                                                               "and 22 characters"),
                                                 EqualTo('new_password', message='The passwords must match exactly')])
    submit = SubmitField("Change Password")


class SendResetEmail(FlaskForm):
    email = EmailField("Email Address", validators=[InputRequired(message="'Email Address' field is required")])
    submit = SubmitField("Send Reset Email")


class ResetPassword(FlaskForm):
    email = EmailField("Your Email", validators=[InputRequired(message="'Your Email' field is required")])
    password = PasswordField("New Password", validators=[InputRequired(message="'New Password' field is required"),
                                                         Length(min=8, max=22, message="Password must be between 8 "
                                                                                       "and 22 characters")])
    confirm_password = PasswordField("Confirm Password",
                                     validators=[InputRequired(message="'Confirm Password' field is required"),
                                                 Length(min=8, max=22, message="Password must be between 8 "
                                                                               "and 22 characters"),
                                                 EqualTo('password', message='Passwords must match exactly')])
    submit = SubmitField("Send Reset Email")


class SubmitTicketForm(FlaskForm):
    issue_subject = StringField("Issue Subject", validators=[InputRequired(message="'Issue Subject' field is required")])
    issue_description = TextAreaField("Description of Issue", validators=[InputRequired(message="'Description of Issue' field is required")])
    submit = SubmitField("Submit")


class CityPriceForm(Form):
    city = StringField("City Name",
                       validators=[InputRequired(message="'City Name' field is required"),
                                   AnyOf(values=city_list,
                                         message="Invalid 'City Name'")])

    price_ceiling = IntegerField("Price Ceiling", validators=[InputRequired(message="'Price Ceiling' field is required"), NumberRange(min=1, message="Price Ceiling must be greater than 0")])


class DestinationForm(FlaskForm):
    search = SearchField("Search field")
    home_airport = StringField("Home Airport", validators=[InputRequired(message="'Home Airport' field is required"),
                                                           AnyOf(values=city_list,
                                                                 message="Invalid 'Home Airport'")])

    currency = SelectField("Currency", choices=['USD', 'EUR', 'SGD', 'AUD', 'THB', 'CNY', 'HUF', 'GBP', 'CAD'],
                           validators=[InputRequired(message="'Currency' field is required")])
    destinations = FieldList(FormField(CityPriceForm), min_entries=3, max_entries=10)


class PreferenceForm(FlaskForm):
    email_frequency = SelectField("Email Frequency", choices=[(1, "Once a week"), (2, "Once every two weeks"),
                                                              (4, "Once a month")], validators=[InputRequired(message="'Email Frequency' field is required")])
    email_day = SelectField("Day of Week to Receive Email",
                            choices=[(0, "Monday"), (1, "Tuesday"), (2, "Wednesday"), (3, "Thursday"),
                                     (4, "Friday"), (5, "Saturday"), (6, "Sunday")])

    cabin_class = SelectField("Cabin Class", choices=[('M', 'Economy'), ('W', 'Premium Economy'),
                                                      ('C', 'Business'), ('F', 'First Class')], validators=[Optional()])
    exclude_airlines = SelectField("Exclude Bad Airlines?",
                                   choices=[('false', 'Include All Airlines'),
                                            ('true', 'Exclude Lowest Rated Airlines')],
                                   validators=[Optional()],
                                   description="Excludes airlines rated lowest in safety, service, claims processing, "
                                               "and punctuality from your flight search (e.g. Ryan Air, EasyJet, "
                                               "Lion Air, China Eastern, Spirit, etc.)")
    max_stops = IntegerField("Max Stops (1-way)",
                             validators=[Optional(), NumberRange(min=0, message="'Max Stops' can't be less than 0")],
                             description="Max number of stops for one-way of the trip. If you have destinations that are remote or quite far from your home airport "
                                         "(overseas, islands, rural cities, etc.), "
                                         "direct flights (i.e. 0 stops) might not be available.")
    max_flight_time = IntegerField("Max Travel Time (1-way)",
                                   validators=[Optional(), NumberRange(min=1, message="'Max Flight Duration' "
                                                                                      "must be greater than 0")],
                                   description="Max number of hours for one-way trip duration. Trip duration includes layovers and stops. If you have destinations that are remote or quite far from your "
                                               "home airport (overseas, islands, rural cities, etc.), "
                                               "short flight times might not be available.")
    ret_to_diff_airport = SelectField("Diff Airport Return?",
                                   choices=[('false', 'Don\'t Include'),
                                            ('true', 'Include')],
                                   validators=[Optional()],
                                      description="Choose whether or not to include flights that return to a different airport than the one from where you departed in your flight results. For example, leaving JFK airport in New York City and returning home to LGA in New York City.")
    num_adults = IntegerField("Adults", validators=[InputRequired(message="'Adults' field is required"), NumberRange(min=1, max=6, message="Number of 'Adult' passengers must be between 1 and 6.")])
    num_children = IntegerField("Children (Age 2-11)", validators=[InputRequired(message="'Children' field is required"), NumberRange(min=0, max=4, message="Number of 'Child' passengers must be between 0 and 4.")])
    num_infants = IntegerField("Infants (Age < 2)", validators=[InputRequired(message="'Infants' field is required"), NumberRange(min=0, max=3, message="Number of 'Infant' passengers must be between 0 and 3.")])
    min_nights = IntegerField("Min Nights", validators=[InputRequired(message="'Min Nights' field is required"), NumberRange(min=0, message="'Min Nights' can't be less than 0.")],
                              description="The minimum possible length of time spent at your travel destination. "
                                          "Actual trip duration might be somewhere in-between the min and max nights")
    max_nights = IntegerField("Max Nights", validators=[InputRequired(message="'Max Nights' field is required"), NumberRange(min=0, message="'Max Nights' can't be less than 0."), invalid_max_nights],
                              description="The maximum possible length of time spent at your travel destination. "
                                          "Actual trip duration might be somewhere in-between the min and max nights")
    search_start_date = SelectField("Search Lead Time", coerce=int,
                                    choices=[(1, 'One day'), (7, 'One week'),
                                             (14, 'Two weeks'), (21, 'Three weeks'), (30, 'One month'),
                                             (60, 'Two months'), (90, 'Three months')],
                                    validators=[InputRequired(message="'Lead Time' field is required")],
                                    description="This is a rolling date, meaning it will move as time passes. "
                                                "For example: If you choose 'two weeks', then if the flight search "
                                                "occurs on March 10th, it will look for flights starting from "
                                                "March 24th onwards.")
    search_length = SelectField("Search Time Window", coerce=int,
                                choices=[(14, 'Two weeks'), (21, 'Three weeks'), (30, 'One month'),
                                         (60, 'Two months'), (90, 'Three months'), (120, 'Four months'),
                                         (150, 'Five months'), (180, 'Six months')],
                                validators=[InputRequired(message="'Time Window' field is required")],
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
