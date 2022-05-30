from flask import flash
from flask_wtf import FlaskForm, Form
from wtforms import *
from wtforms.validators import *
from datetime import timedelta, date
from iata_codes import all_cities_international

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
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class CityPriceForm(Form):
    city = StringField("City Name",
                       validators=[DataRequired(),
                                   AnyOf(values=city_list,
                                         message="Please select one of the choices shown as you type.")])

    price_ceiling = IntegerField("Price Ceiling", validators=[DataRequired()])


class DestinationForm(FlaskForm):
    search = SearchField("Search field")
    home_airport = StringField("Home Airport Code", validators=[DataRequired(), Length(min=3, max=3)], description="The 3 letter code for the airport that you fly out from")
    currency = SelectField("Currency", choices=['USD', 'EUR', 'SGD', 'AUD', 'THB', 'CNY', 'HUF', 'GBP', 'CAD'],
                           validators=[DataRequired()])
    destinations = FieldList(FormField(CityPriceForm), min_entries=3, max_entries=10)


class PreferenceForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    email_frequency = SelectField("Email Frequency", choices=[(1, "Once a week"), (2, "Once every two weeks"), (4, "Once a month")], validators=[DataRequired()])
    email_day = SelectField("Day of Week to Receive Email",
                            choices=[(0, "Monday"), (1, "Tuesday"), (2, "Wednesday"), (3, "Thursday"), (4, "Friday"), (5, "Saturday"), (6, "Sunday")])
    min_nights = IntegerField("Trip Duration: Minimum Number of Nights", validators=[DataRequired(), NumberRange(min=0)], description="The minimum length of time spent at your travel destination.")
    max_nights = IntegerField("Trip Duration: Max Number of Nights", validators=[DataRequired(), NumberRange(min=0)], description="The maximum length of time spent at your travel destination. Actual trip duration will be somewhere in-between the min and max duration")
    cabin_class = SelectField("Cabin Class", choices=[('', 'Select Option'),('M', 'Economy'), ('W', 'Premium Economy'), ('C', 'Business'), ('F', 'First Class')], validators=[Optional()])
    exclude_airlines = SelectField("Exclude Lowest Rated/Cheapo Airlines?", choices=[("Select Option", 'Select Option'), ('True', 'Exclude'), ('False', 'Include The Cheapos')], validators=[Optional()], description="Excludes lowest rated airlines in safety and service from flight search")
    max_stops = IntegerField("Max Number of Stops (One Way)", validators=[Optional(), NumberRange(min=0, max=6)])
    max_flight_time = IntegerField("Max Flight Duration", validators=[Optional()])
    num_adults = IntegerField("Number of Adult Passengers", validators=[Optional(), NumberRange(min=1, max=6)])
    num_children = IntegerField("Number of Child Passengers (Age 2-11)", validators=[Optional(), NumberRange(min=0, max=4)])
    num_infants = IntegerField("Number of Infant Passengers (Age < 2)", validators=[Optional(), NumberRange(min=0, max=3)])
    search_start_date = SelectField("How far out should the flight search begin looking for flights", coerce=int,
                                    choices=[(1, 'One day'), (7, 'One week'),
                                             (14, 'Two weeks'), (21, 'Three weeks'), (30, 'One month'),
                                             (60, 'Two months'), (90, 'Three months'),
                                             (0, 'Specific Start Date? Use the input below')],
                                    validators=[DataRequired()], description="Note: This is a rolling date range, meaning it will move as time passes. Since Flight Club searches flights weekly, this is better than a specific date range.")
    specific_search_start_date = DateField('Alternatively, choose a specific Start Date', validators=[Optional(), invalid_date],
                                           description="Note: This is a fixed date which will not move as time passes. Choose this if you only have specific date ranges available to travel (holidays, summer, etc.)")
    search_length = SelectField("Search Date Range (the window of time flights will be searched)", coerce=int,
                                choices=[(7, 'One week'), (14, 'Two weeks'), (21, 'Three weeks'), (30, 'One month'), (60, 'Two months'), (90, 'Three months'), (120, 'Four months'),
                                         (0, 'Specific End Date? Use the input below')], validators=[DataRequired()],
                                description="Note: This is also a rolling date range, meaning it will move as time passes. For example, if it begins looking for flights 'One month' out and has a date range of '3 months', then if it searches on June 10th, it would look for all flights between July 10th and October 10th.")
    specific_search_end_date = DateField('Alternatively, choose a specific End Date',
                                           validators=[Optional(), invalid_date, date_range_check], description="Note: This is a fixed date which will not move as time passes. Choose this if you only have specific date ranges available to travel (holidays, summer, etc.)")
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

