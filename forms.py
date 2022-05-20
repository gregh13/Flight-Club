from flask_wtf import FlaskForm, Form
from wtforms import *
from wtforms.validators import *


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


class CityPriceForm(Form):
    city = StringField("City Name", validators=[DataRequired()])
    price_ceiling = IntegerField("Price Ceiling", validators=[DataRequired(), NumberRange(min=1)])


class DestinationForm(FlaskForm):
    home_airport = StringField("Home Airport Code", validators=[DataRequired(), Length(min=3, max=3)], description="The 3 letter code for the airport that you fly out from")
    destinations = FieldList(FormField(CityPriceForm), min_entries=3, max_entries=10)


class PreferenceForm(FlaskForm):
    home_airport = StringField("Home Airport Code (ex: SFO, PHX, SIN, BKK)", validators=[DataRequired(), Length(min=3, max=3)], description="The 3 letter code for the airport that you fly out from")
    min_nights = IntegerField("Trip Duration: Minimum Number of Nights", validators=[DataRequired(), NumberRange(min=0)], description="The minimum length of time spent at your travel destination.")
    max_nights = IntegerField("Trip Duration: Max Number of Nights", validators=[DataRequired(), NumberRange(min=0)], description="The maximum length of time spent at your travel destination. Actual trip duration will be somewhere in-between the min and max duration")
    currency = SelectField("Currency", choices=['Select Option','USD', 'SGD', 'AUD', 'THB', 'CNY', 'GBP', 'CAD'], validators=[DataRequired()])
    cabin_class = SelectField("Cabin Class", choices=[('Select Option', 'Select Option'),('M', 'Economy'), ('W', 'Premium Economy'), ('C', 'Business'), ('F', 'First Class')], validators=[Optional()])
    mix_class = SelectField("Mix Cabin Class?", choices=['Select Option', 'Yes', 'No'], validators=[Optional()], description="Mainly only applies when choosing a higher class than economy.")
    exclude_airlines = SelectField("Exclude Lowest Rated/Cheapo Airlines?", choices=['Select Option','Exclude', 'Include The Cheapos'], validators=[Optional()], description="Excludes lowest rated airlines in safety and service from flight search")
    flight_type = SelectField("Flight Type", choices=[('round', 'Round Trip'), ('oneway', 'One Way')], validators=[Optional()])
    max_stops = IntegerField("Max Number of Stops", validators=[Optional(), NumberRange(min=0, max=6)])
    max_flight_time = IntegerField("Max Flight Duration", validators=[Optional()])
    num_adults = IntegerField("Number of Adult Passengers", validators=[Optional(), NumberRange(min=0, max=6)])
    num_children = IntegerField("Number of Child Passengers", validators=[Optional(), NumberRange(min=0, max=6)])
    num_infants = IntegerField("Number of Infant Passengers", validators=[Optional(), NumberRange(min=0, max=6)])
    search_start_date = SelectField("How far out should the flight search begin looking for flights", coerce=int,
                                    choices=[(111, 'Select Option'), (1, 'One day -- (last minute getaway?)'), (7, 'One week -- (spontaneous weekend trip)'),
                                             (14, 'Two weeks'), (21, 'Three weeks'), (30, 'One month -- (some time to plan, get time off work)'),
                                             (60, 'Two months'), (90, 'Three months -- (plenty of time to prepare)'),
                                             (0, 'Specific Start Date? Use the input below')],
                                    validators=[DataRequired()], description="Note: This is a rolling date range, meaning it will move as time passes. Since Flight Club searches flights weekly, this is better than a specific date range.")
    specific_search_start_date = DateField('Alternatively, choose a specific Start Date', validators=[Optional()],
                                           description="Note: This is a fixed date which will not move as time passes. Choose this if you only have specific date ranges available to travel (holidays, summer, etc.)")
    search_length = SelectField("Search Date Range (the window of time flights will be searched)", coerce=int,
                                choices=[(111, 'Select Option'), (7, 'One week'), (14, 'Two weeks'), (21, 'Three weeks'), (30, 'One month'), (60, 'Two months'), (90, 'Three months'), (120, 'Four months'),
                                         (0, 'Specific End Date? Use the input below')], validators=[DataRequired()],
                                description="Note: This is also rolling date range, meaning it will move as time passes. For example, if it begins looking for flights 'One month' out and has a date range of '3 months', then if it searched on June 10th, it would look for all flights between July 10th and October 10th.")
    specific_search_end_date = DateField('Alternatively, choose a specific End Date',
                                           validators=[Optional()], description="Note: This is a fixed date which will not move as time passes. Choose this if you only have specific date ranges available to travel (holidays, summer, etc.)")
    submit = SubmitField("Update Preferences")


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

