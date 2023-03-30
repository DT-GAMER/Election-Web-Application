from flask import render_template
from app import app, db
from models import Candidate, Vote

def calculate_results():
    # get a list of all the positions
    positions = db.session.query(Candidate.position).distinct()

    # create a dictionary to store the results
    results = {}

    # loop through the positions and calculate the results for each one
    for position in positions:
        # get a list of all the candidates for this position
        candidates = db.session.query(Candidate).filter(Candidate.position == position).all()

        # get the total number of votes cast for this position
        total_votes = db.session.query(Vote).filter(Vote.candidate.in_(candidates)).count()

        # get a count of the votes for each candidate
        candidate_votes = db.session.query(Vote.candidate, func.count(Vote.id)).filter(Vote.candidate.in_(candidates)).group_by(Vote.candidate).all()

        # create a list of tuples containing the candidate name and their vote count
        results[position] = [(c.name, v) for c, v in candidate_votes]

        # add the total number of votes to the results dictionary
        results[position].append(('Total Votes', total_votes))

    return results

@app.route('/results')
def results():
    # calculate the election results
    results = calculate_results()

    # render the results template with the results
    return render_template('results.html', results=results)
