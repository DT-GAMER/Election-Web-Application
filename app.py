from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from datetime import datetime
from models import db, User, Position, Candidate, Vote
from forms import SignUpForm, LoginForm, VoteForm
from authentication import login_required, current_user, logout_user
from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
db =SQLAlchemy(app)
migrate = Migrate(app, db)
cors = CORS(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        email = form.email.data
        names = form.names.data
        password = form.password.data
        user = User(email=email, names=names, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            flash('You have been logged in!', 'success')
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Log In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    positions = Position.query.all()
    votes = Vote.query.all()
    return render_template('dashboard.html', title='Dashboard', positions=positions, votes=votes)

@app.route('/candidates')
@cross_origin()
def candidates():
    candidates = Candidate.query.all()
    return jsonify({'candidates': [{'id': c.id, 'name': c.name, 'position': c.position} for c in candidates]})

@app.route('/vote', methods=['GET', 'POST'])
@login_required
def vote():
    form = VoteForm()
    if form.validate_on_submit():
        position_id = form.position.data
        candidate_id = form.candidate.data
        user_id = current_user.id
        existing_vote = Vote.query.filter_by(user_id=user_id, position_id=position_id).first()
        if existing_vote:
            flash('You have already voted for this position', 'danger')
        else:
            vote = Vote(user_id=user_id, position_id=position_id, candidate_id=candidate_id)
            db.session.add(vote)
            db.session.commit()
            flash('Your vote has been recorded!', 'success')
            return redirect(url_for('dashboard'))
    positions = Position.query.all()
    form.position.choices = [(p.id, p.title) for p in positions]
    form.candidate.choices = [(c.id, c.names) for c in Candidate.query.all()]
    return render_template('vote.html', title='Vote', form=form)


@app.route('/results')
@login_required
def results():
    positions = Position.query.all()
    votes = Vote.query.all()
    results = []
    for position in positions:
        candidates = Candidate.query.filter_by(position_id=position.id).all()
        position_results = {}
        position_results['title'] = position.title
        position_results['candidates'] = []
        for candidate in candidates:
            candidate_results = {}
            candidate_results['name'] = candidate.names
            candidate_results['votes'] = len([v for v in votes if v.candidate_id == candidate.id])
            position_results['candidates'].append(candidate_results)
        results.append(position_results)
    return render_template('results.html', title='Results', results=results)

@app.route('/')
def application_great():
    return 'This application is great!'

if __name__ == 'main':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

