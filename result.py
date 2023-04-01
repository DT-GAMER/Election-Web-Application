from app import db
from models import Candidate, Vote

def calculate_results():
    """Calculates the results of the election and returns them as a dictionary."""
    results = {}

    # Get all the candidates and their positions
    candidates = Candidate.query.all()
    positions = set(candidate.position for candidate in candidates)

    # Calculate the votes for each position
    for position in positions:
        position_candidates = [candidate for candidate in candidates if candidate.position == position]
        position_votes = [vote for vote in Vote.query.all() if vote.candidate in position_candidates]
        position_results = {}

        # Calculate the vote count and percentage for each candidate
        total_votes = len(position_votes)
        for candidate in position_candidates:
            candidate_votes = len([vote for vote in position_votes if vote.candidate == candidate])
            candidate_percentage = round((candidate_votes / total_votes) * 100, 2)
            position_results[candidate.name] = {"votes": candidate_votes, "percentage": candidate_percentage}

        # Determine the winner for this position
        winner = max(position_results.items(), key=lambda x: x[1]["votes"])
        results[position] = {"winner": winner[0], "results": position_results}

    return results
