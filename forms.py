
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class RegistrationForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=255)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=255)])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    voter_id = StringField('Voter ID', validators=[DataRequired()])
    voter_key = PasswordField('Voter Key', validators=[DataRequired()])
    submit = SubmitField('Login')
