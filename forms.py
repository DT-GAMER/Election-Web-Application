from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataReqiuired(), Length(min=15)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    full_name = StringField('Full Name', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class VoteForm(FlaskForm):
    general_secretary = RadioField('General Secretary', choices=[('Joy Ifeanyi Dennis(John Wick)')], validators=[DataRequied()])
    treasurer = RadioField('Treasurer', choices=[('Taiwo Elizabeth Fowowde')], validators=[DataRequired()])
    sport_secretary = RadioField('Sport Secretary', choices=[('Alli_Kammal Mazeedah', 'Ayo Babalola(Ghost)', 'Farinloye Susan Folake')], validators=[DataRequired()])
    public_relations_officer = RadioField('Public Relations Officer', choices=[('Annaun Samuel')], validators=[DataRequired()])
    social_secretary = RadioField('Social Secretary', choices=[('Shoneye Omolola', 'Akintunde Itunuoluwa', 'Akinyomi Sefunmi Isaiah')], validators=[DataRequired()])
    financial_secretary = RadioField('Financial Secretary' choices=[('Moghalu Chinyere')], validators=[DataRequired()])
    welfare_secretary = RadioField('Welfare Secretary' choices=[('Yusuf Aminat', 'Victoria Olomola')], validators=[DataRequired()])
    assistant_general_secretary = RadioField('Assistant General Secretary', choices=[('Oyeyinka Sarah')], validators=[DataRequired()])
    submit = SubmitField('vote')
