from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        voter_id = request.form.get('voter_id')
        voter_key = request.form.get('voter_key')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(voter_id=voter_id).first()

        if not user or not check_password_hash(user.voter_key, voter_key):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)
        return redirect(url_for('main.index'))

    return render_template('login.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        voter_id = generate_voter_id()
        voter_key = generate_random_password()

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))

        new_user = User(full_name=full_name, email=email, voter_id=voter_id, voter_key=generate_password_hash(voter_key, method='sha256'))

        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Your voter ID is {0} and voter key is {1}. Keep them safe.'.format(voter_id, voter_key))

        return redirect(url_for('auth.login'))

    return render_template('signup.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


def generate_voter_id():
    # generating a random 8-digit integer
    import random
    return str(random.randint(10000000, 99999999))


def generate_random_password(length=10):
    # generating a random alphanumeric string of length 10
    import string
    import secrets
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(length))

