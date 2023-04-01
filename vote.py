from flask import Blueprint, render_template, redirect, url_for, request, flash, session

from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime, time

from app import db

from models import Candidate, Voter, Vote

vote_bp = Blueprint('vote', __name__, url_prefix='/vote')

# Voting page

@vote_bp.route('/', methods=['GET', 'POST'])

def voting():

    if request.method == 'POST':

        # Get the selected candidate IDs from the form

        selected_candidates = request.form.getlist('candidate')

        # Check if user has already voted

        voter_id = session.get('voter_id')

        if Vote.query.filter_by(voter_id=voter_id).first() is not None:

            flash('You have already voted!', 'error')

            return redirect(url_for('vote.voting'))

        # Create a new Vote object for each selected candidate

        for candidate_id in selected_candidates:

            vote = Vote(voter_id=voter_id, candidate_id=candidate_id)

            db.session.add(vote)

        db.session.commit()

        # Redirect to confirmation page

        return redirect(url_for('vote.confirmation'))

    # Get the list of candidates

    candidates = Candidate.query.all()

    # Render the voting page

    return render_template('voting.html', candidates=candidates)

# Confirmation page

@vote_bp.route('/confirmation')

def confirmation():

    return render_template('confirmation.html')

