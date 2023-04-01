from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField,  SubmitField
from wtforms.validators import DataRequired, Email, Length


class RegistrationForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=255)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=255)])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    voter_id = StringField('Voter ID', validators=[DataRequired()])
    voter_key = PasswordField('Voter Key', validators=[DataRequired()])
    submit = SubmitField('Login')


class VoteForm(FlaskForm):
    social_secretary = RadioField('Social Secretary', choices=[('shoneye_omolola', 'Shoneye Omolola Serah'), ('akintunde_itunuoluwapo', 'Akintunde Itunuoluwapo Anjolaoluna')])
    public_relations_officer = RadioField('Public Relations Officer', choices=[('annaun_samuel', 'Annaun Samuel')])
    financial_secretary = RadioField('Financial Secretary', choices=[('muoghalu_chinyere', 'Muoghalu Chinyere Love')])
    sport_secretary = RadioField('Sport Secretary', choices=[('farinloye_folake', 'Farinloye Folake Susan'), ('alli_kamal', 'Alli-Kamal Mazeedah Oyindamola'), ('babalola_ayoola', 'Babalola Ayoola Samuel')])
    welfare_secretary = RadioField('Welfare Secretary', choices=[('olomola_victoria', 'Olomola Victoria Ayomide'), ('yusuf_aminat', 'Yusuf Aminat Opeyemi'), ('akinyomi_sefunmi', 'Akinyomi Sefunmi Isaiah')])
    assistant_general_secretary = RadioField('Assistant General Secretary', choices=[('oyeyinka_oluwapelumi', 'Oyeyinka Oluwapelumi Sarah')])
    treasurer = RadioField('Treasurer', choices=[('taiwo_elizabeth', 'Taiwo Elizabeth Fowode')])
    submit = SubmitField('vote')
