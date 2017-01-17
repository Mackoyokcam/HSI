from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, FloatField, HiddenField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class AccountCreationForm(Form):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=25)], render_kw={"placeholder": "First Name"})
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=25)], render_kw={"placeholder": "Last Name"})
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=35)], render_kw={"placeholder": "Email Address"})
    password = PasswordField('New Password', validators=[DataRequired(),
            EqualTo('confirm', message='Passwords must match')], render_kw={"placeholder": "New Password"})
    confirm = PasswordField('Repeat Password', validators=[DataRequired()], render_kw={"placeholder": "Confirm Password"})
    address = StringField('Address', validators=[DataRequired()], render_kw={"placeholder": "Address"})
    apt = StringField('Apartment', validators=[DataRequired()], render_kw={"placeholder": "Apartment #"})
    city = StringField('City', validators=[DataRequired()], render_kw={"placeholder": "City"})
    state = StringField('State', validators=[DataRequired()], render_kw={"placeholder": "State"})
    zip = StringField('Zip', validators=[DataRequired()], render_kw={"placeholder": "Zip"})
    rent = FloatField('Rent', validators=[DataRequired()], render_kw={"placeholder": "Rent"})
    gas = FloatField('Gas', validators=[DataRequired()], render_kw={"placeholder": "Gas Bill"})
    water = FloatField('Water', validators=[DataRequired()], render_kw={"placeholder": "Water Bill"})
    heating = FloatField('Heating', validators=[DataRequired()], render_kw={"placeholder": "Heating Bill"})
    electrical = FloatField('Electrical', validators=[DataRequired()], render_kw={"placeholder": "Electrical Bill"})
    recycle = BooleanField('Recycle?')
    compost = BooleanField('Compost?')


