from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, FloatField, HiddenField, validators
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp


class AccountCreationForm(Form):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=25),
                                                       Regexp('^[a-zA-Z0-9\s]*$',
                                                              message="Please use only alphanumeric characters.")],
                             render_kw={"placeholder": "First Name"})
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=25),
                                                     Regexp('^[a-zA-Z0-9\s]*$',
                                                            message="Please use only alphanumeric characters.")],
                            render_kw={"placeholder": "Last Name"})
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=35)],
                        render_kw={"placeholder": "Email Address"})
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=6),
                                                         EqualTo('confirm', message='Passwords must match')],
                             render_kw={"placeholder": "New Password"})
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=6)],
                            render_kw={"placeholder": "Confirm Password"})


class AddressForm(Form):
    address = StringField('Address', validators=[DataRequired(), Regexp('^[a-zA-Z0-9\s]*$',
                                                                        message="Please use only alphanumeric characters.")],
                          render_kw={"placeholder": "Address"})
    apt = StringField('Apartment', validators=[DataRequired(), Regexp('^[a-zA-Z0-9]*$',
                                                                        message="Please use only alphanumeric characters.")],
                      render_kw={"placeholder": "Apartment #"})
    city = StringField('City', validators=[DataRequired(), Regexp('^[a-zA-Z0-9\s]*$',
                                                                        message="Please use only alphanumeric characters.")],
                       render_kw={"placeholder": "City"})
    state = StringField('State', validators=[DataRequired(), Regexp('^[a-zA-Z0-9\s]*$',
                                                                        message="Please use only alphanumeric characters.")],
                        render_kw={"placeholder": "State"}, )
    zip = StringField('Zip', validators=[DataRequired(), Regexp('^\d{5}(?:[-\s]\d{4})?$',
                                                                        message="Not a valid zip code.")],
                      render_kw={"placeholder": "Zip"})
    rent = FloatField('Rent', validators=[DataRequired(message='Please enter a decimal value (ie 100, 100.0).')],
                      render_kw={"placeholder": "Rent"})
    gas = FloatField('Gas', validators=[DataRequired(message='Please enter a decimal value (ie 100, 100.0).')],
                     render_kw={"placeholder": "Gas Bill"})
    water = FloatField('Water', validators=[DataRequired(message='Please enter a decimal value (ie 100, 100.0).')],
                       render_kw={"placeholder": "Water Bill"})
    heating = FloatField('Heating', validators=[DataRequired(message='Please enter a decimal value (ie 100, 100.0).')],
                         render_kw={"placeholder": "Heating Bill"})
    electrical = FloatField('Electrical', validators=[DataRequired(message='Please enter a decimal value (ie 100, 100.0).')],
                            render_kw={"placeholder": "Electrical Bill"})
    recycle = BooleanField('Recycle?')
    compost = BooleanField('Compost?')

# not currently used
class AddressSearchForm(Form):
    address = StringField('Address', validators=[DataRequired()], render_kw={})
