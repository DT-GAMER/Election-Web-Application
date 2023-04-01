from flask import Flask, Blueprint, render_template, redirect, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import LoginForm, VoteForm, RegistrationForm
from models import User, Candidate, Vote
from werkzeug.security import generate_password_hash
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
        user = User.query.filter_by(voter_id=form.voter_id.data).first()
        if user and bcrypt.checkpw(form.voter_key.data.encode(), user.voter_key.encode()):
            session['user'] = user.id
            session.permanent = True
            return redirect('/dashboard')
        else:
            flash('Invalid Voter ID or Key', 'error')
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

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Email address already exists')
            return redirect(url_for('auth.register'))
        else:
            # generate a random voter id and key for the new user
            voter_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            voter_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            
            new_user = User(full_name=form.full_name.data, email=form.email.data,
                            password=generate_password_hash(form.password.data, method='sha256'),
                            voter_id=voter_id, voter_key=voter_key)
            new_user.save()
            flash('Registration successful. Please log in.')
            return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@app.route('/')
def application_great():
    return 'This application is great!'

if __name__ == 'main':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
