from flask import render_template
from app import app, db
from models import Position, Candidate, Vote

@app.route('/dashboard')
def dashboard():
    """Displays the election dashboard."""
    # Get all positions from the database
    positions = Position.query.all()

    # Get the total number of votes cast
    total_votes = db.session.query(Vote).count()

    # Get the number of votes for each candidate
    candidate_votes = {}
    for candidate in Candidate.query.all():
        candidate_votes[candidate.id] = candidate.votes.count()

    # Get the winner for each position
    winners = {}
    for position in positions:
        candidates = position.candidates
        if candidates:
            winner = max(candidates, key=lambda c: candidate_votes[c.id])
            winners[position.id] = winner

    # Render the dashboard template with the election data
    return render_template('dashboard.html', positions=positions, total_votes=total_votes, candidate_votes=candidate_votes, winners=winners)
