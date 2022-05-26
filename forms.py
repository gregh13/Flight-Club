from flask_wtf import FlaskForm, Form
from wtforms import *
from wtforms.validators import *
from codes import all_cities_international


possible_cities = {'SFO': 'San Francisco', 'BKK': 'Bangkok (BKK)', 'DMK': 'Bangkok(DMK)',
                   'SIN': 'Singapore', 'SMF': 'Sacramento', 'MLE': 'Male (Maldives)', 'BUD': 'Budapest',
                   'CDG': 'Paris (CDG)', 'TPE': 'Taipei', 'SYD': 'Sydney'}
city_list = [all_cities_international[iata] for iata in all_cities_international]


# # WTForm
class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class TrialForm(FlaskForm):
    trial = StringField("Trial", validators=[AnyOf(values=city_list, message="Please select one of the choices shown as you type")])
    submit = SubmitField("Submit")


# class CityPriceForm(Form):
#     city = SelectField("City Name",
#                        choices=[("", "")] + [(iata, city) for iata, city in all_cities_international.items()],
#                        # [("", "")] is needed for a placeholder
#                        validators=[InputRequired()])
#     price_ceiling = IntegerField("Price Ceiling", validators=[DataRequired()])


class CityPriceForm(Form):
    city = StringField("City Name", validators=[DataRequired(),
                                                AnyOf(values=city_list,
                                                      message="Please select one of the choices shown as you type.")])
    price_ceiling = IntegerField("Price Ceiling", validators=[DataRequired()])


class DestinationForm(FlaskForm):
    search = SearchField("Search field")
    home_airport = StringField("Home Airport Code", validators=[DataRequired(), Length(min=3, max=3)], description="The 3 letter code for the airport that you fly out from")
    destinations = FieldList(FormField(CityPriceForm), min_entries=3, max_entries=10)


class PreferenceForm(FlaskForm):
    email_frequency = SelectField("Email Frequency", choices=[(111, 'Select Option'), (1, "Once a week"), (2, "Once every two weeks"), (4, "Once a month")], validators=[DataRequired()])
    min_nights = IntegerField("Trip Duration: Minimum Number of Nights", validators=[DataRequired(), NumberRange(min=0)], description="The minimum length of time spent at your travel destination.")
    max_nights = IntegerField("Trip Duration: Max Number of Nights", validators=[DataRequired(), NumberRange(min=0)], description="The maximum length of time spent at your travel destination. Actual trip duration will be somewhere in-between the min and max duration")
    currency = SelectField("Currency", choices=['Select Option', 'USD', 'SGD', 'AUD', 'THB', 'CNY', 'GBP', 'CAD'], validators=[DataRequired()])
    cabin_class = SelectField("Cabin Class", choices=[('Select Option', 'Select Option'),('M', 'Economy'), ('W', 'Premium Economy'), ('C', 'Business'), ('F', 'First Class')], validators=[Optional()])
    exclude_airlines = SelectField("Exclude Lowest Rated/Cheapo Airlines?", choices=['Select Option', 'Exclude', 'Include The Cheapos'], validators=[Optional()], description="Excludes lowest rated airlines in safety and service from flight search")
    flight_type = SelectField("Flight Type", choices=[('select', 'Select Option'), ('round', 'Round Trip'), ('oneway', 'One Way')], validators=[Optional()])
    max_stops = IntegerField("Max Number of Stops", validators=[Optional(), NumberRange(min=0, max=6)])
    max_flight_time = IntegerField("Max Flight Duration", validators=[Optional()])
    num_adults = IntegerField("Number of Adult Passengers", validators=[Optional(), NumberRange(min=0, max=6)])
    num_children = IntegerField("Number of Child Passengers", validators=[Optional(), NumberRange(min=0, max=6)])
    num_infants = IntegerField("Number of Infant Passengers", validators=[Optional(), NumberRange(min=0, max=6)])
    search_start_date = SelectField("How far out should the flight search begin looking for flights", coerce=int,
                                    choices=[(111, 'Select Option'), (1, 'One day'), (7, 'One week'),
                                             (14, 'Two weeks'), (21, 'Three weeks'), (30, 'One month'),
                                             (60, 'Two months'), (90, 'Three months'),
                                             (0, 'Specific Start Date? Use the input below')],
                                    validators=[DataRequired()], description="Note: This is a rolling date range, meaning it will move as time passes. Since Flight Club searches flights weekly, this is better than a specific date range.")
    specific_search_start_date = DateField('Alternatively, choose a specific Start Date', validators=[Optional()],
                                           description="Note: This is a fixed date which will not move as time passes. Choose this if you only have specific date ranges available to travel (holidays, summer, etc.)")
    search_length = SelectField("Search Date Range (the window of time flights will be searched)", coerce=int,
                                choices=[(111, 'Select Option'), (7, 'One week'), (14, 'Two weeks'), (21, 'Three weeks'), (30, 'One month'), (60, 'Two months'), (90, 'Three months'), (120, 'Four months'),
                                         (0, 'Specific End Date? Use the input below')], validators=[DataRequired()],
                                description="Note: This is also a rolling date range, meaning it will move as time passes. For example, if it begins looking for flights 'One month' out and has a date range of '3 months', then if it searches on June 10th, it would look for all flights between July 10th and October 10th.")
    specific_search_end_date = DateField('Alternatively, choose a specific End Date',
                                           validators=[Optional()], description="Note: This is a fixed date which will not move as time passes. Choose this if you only have specific date ranges available to travel (holidays, summer, etc.)")
    submit = SubmitField("Save Changes")


#
# class NumberDestinationsForm(Form):
#     location_id = StringField('location_id')
#     city = StringField('city')
#
# class CompanyForm(Form):
#     company_name = StringField('company_name')
#     locations = FieldList(FormField(LocationForm))





#
# class CreatePostForm(FlaskForm):
#     title = StringField("Blog Post Title", validators=[DataRequired()])
#     subtitle = StringField("Subtitle", validators=[DataRequired()])
#     img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
#     body = CKEditorField("Blog Content", validators=[DataRequired()])
#     submit = SubmitField("Submit Post")
#
# class CommentForm(FlaskForm):
#     comment_text = CKEditorField("Post A Comment", validators=[DataRequired()])
#     submit = SubmitField("Submit Comment")

