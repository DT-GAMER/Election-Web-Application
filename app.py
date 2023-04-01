from flask import Flask, Blueprint, render_template, redirect, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import LoginForm, VoteForm, RegistrationForm
from models import User, Candidate, Vote, position
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt
import random
import string

auth = Blueprint('auth', __name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'

db = SQLAlchemy(app)

# CORS setup
from flask_cors import CORS
CORS(app)



# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        voter_id = form.voter_id.data
        voter_key = form.voter_key.data

        # Check if voter exists in the database
        voter = Voter.query.filter_by(voter_id=voter_id).first()
        if voter:
            # Validate voter's key
            if check_password_hash(voter.voter_key, voter_key):
                # Create session for the voter
                session['logged_in'] = True
                session['voter_id'] = voter_id

                flash('You have successfully logged in.', 'success')
                return redirect(url_for('vote'))
 
        flash('Invalid voter ID or key.', 'error')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    user = User.query.get(session['user'])
    if not user:
        return redirect('/login')
    if not user.has_voted:
        positions = Candidate.query.with_entities(Candidate.position).distinct().all()
        return render_template('vote.html', positions=positions)
    else:
        votes = Vote.query.filter_by(user_id=user.id).all()
        return render_template('results.html', votes=votes)

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if 'user' not in session:
        return redirect('/login')
    user = User.query.get(session['user'])
    if not user:
        return redirect('/login')
    if user.has_voted:
        flash('You have already voted', 'error')
        return redirect('/dashboard')
    form = VoteForm()
    if form.validate_on_submit():
        for position, candidate_id in form.data.items():
            if position.startswith('position_'):
                position_name = position.split('position_')[1]
                candidate = Candidate.query.filter_by(id=candidate_id).first()
                if candidate:
                    vote = Vote(user_id=user.id, position=position_name, candidate_id=candidate_id)
                    db.session.add(vote)
        user.has_voted = True
        db.session.commit()
        flash('Vote casted successfully!', 'success')
        return redirect('/dashboard')
    else:
        positions = Candidate.query.with_entities(Candidate.position).distinct().all()
        candidates = {}
        for position in positions:
            candidates[position[0]] = Candidate.query.filter_by(position=position[0]).all()
        return render_template('vote.html', positions=positions, candidates=candidates, form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('This email address has already been used to register.')
            return redirect(url_for('register'))
        else:
            # Generate unique voter's ID
            voter_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            # Generate random password for voter key
            voter_key = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=20))
            # Save user to database with generated voter ID and key
            new_user = User(name=form.name.data, email=form.email.data, voter_id=voter_id, voter_key=generate_password_hash(voter_key))
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. Your Voter ID is {} and Voter Key is {}.'.format(voter_id, voter_key))
            return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/')
def application_great():
    return 'This application is great!'

if __name__ == 'main':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
