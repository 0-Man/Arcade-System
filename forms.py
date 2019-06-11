from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    fName = StringField('First Name',
                validators=[DataRequired(), Length(min=2, max=20)])
    lName = StringField('Last Name',
                validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email',
                validators=[DataRequired(), Email()])
    phone = StringField('Phone',
                validators=[DataRequired(), Length(min=10, max=15)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                validators=[DataRequired(), EqualTo('password')])
    type = SelectField('Type', choices = [('Administrator'), ('Employee'), ('Member')])
    minutes = IntegerField('Minutes (default = 0)')
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    type = SelectField('Type', choices = [('Administrator'), ('Employee'), ('Member')])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class TransactionForm(FlaskForm):
    payment = BooleanField('Credit? (default = Cash)')
    amount  = IntegerField('Total Cost')
    product = StringField('Product Names', validators=[DataRequired()])
    id = IntegerField('User-id')
    submit = SubmitField('Checkout')
