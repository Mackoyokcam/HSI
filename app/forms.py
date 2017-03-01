from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, FloatField, HiddenField, validators, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp, InputRequired, ValidationError
import time


class Login(Form):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=35)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    rememberMe = BooleanField('Remember me')


class AccountCreationForm(Form):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=25),
                                                       Regexp('^[a-zA-Z0-9\s]*$',
                                                              message="Please use only alphanumeric characters.")])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=25),
                                                     Regexp('^[a-zA-Z0-9\s]*$',
                                                            message="Please use only alphanumeric characters.")])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=35)])
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=6),
                                                         EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=6)])


class AddressForm(Form):
    address = StringField('Address', validators=[DataRequired(), Regexp('^[a-zA-Z0-9\s]*$',
                                                                        message="Please use only alphanumeric characters.")])
    apt = StringField('Apartment', validators=[DataRequired(), Regexp('^[a-zA-Z0-9]*$',
                                                                        message="Please use only alphanumeric characters.")])
    city = StringField('City', validators=[DataRequired(), Regexp('^[a-zA-Z0-9\s]*$',
                                                                        message="Please use only alphanumeric characters.")])
    state = StringField('State', validators=[DataRequired(), Regexp('^[a-zA-Z0-9\s]*$',
                                                                        message="Please use only alphanumeric characters.")])
    zip = StringField('Zip', validators=[DataRequired(), Regexp('^\d{5}(?:[-\s]\d{4})?$',
                                                                        message="Not a valid zip code.")])
    rent = FloatField('Rent', validators=[InputRequired()])
    gas = FloatField('Gas', validators=[InputRequired()])
    water = FloatField('Water', validators=[InputRequired()])
    electrical = FloatField('Electrical', validators=[InputRequired()])
    recycle = BooleanField('Recycle?')
    compost = BooleanField('Compost?')
    updateDate = StringField('', render_kw={"value": time.strftime("%Y.%m.%d"), "hidden": True})


class OriginCompareForm(Form):

    address1 = StringField('Address', validators=[DataRequired(), Regexp('^[a-zA-Z0-9\s]*$',
                                                                        message="Please use only alphanumeric characters.")])
    city1 = StringField('City', validators=[DataRequired(), Regexp('^[a-zA-Z0-9\s]*$',
                                                              message="Please use only alphanumeric characters.")])
    state1 = StringField('State', validators=[DataRequired(), Regexp('^[a-zA-Z0-9\s]*$',
                                                                message="Please use only alphanumeric characters.")])
    zip1 = StringField('Zip', validators=[DataRequired(), Regexp('^\d{5}(?:[-\s]\d{4})?$',
                                                            message="Not a valid zip code.")])

    
class DestinationCompareForm(Form):

    address1 = StringField('Address', validators=[DataRequired(), Regexp('^[a-zA-Z0-9\s]*$',
                                                                        message="Please use only alphanumeric characters.")])
    city1 = StringField('City', validators=[DataRequired(), Regexp('^[a-zA-Z0-9\s]*$',
                                                              message="Please use only alphanumeric characters.")])
    state1 = StringField('State', validators=[DataRequired(), Regexp('^[a-zA-Z0-9\s]*$',
                                                                message="Please use only alphanumeric characters.")])
    zip1 = StringField('Zip', validators=[DataRequired(), Regexp('^\d{5}(?:[-\s]\d{4})?$',
                                                            message="Not a valid zip code.")])


# not currently used
class AddressSearchForm(Form):
    address = StringField('Address', validators=[DataRequired()], render_kw={"placeholder": "Search Address"})
