from flask import Flask, render_template, redirect, url_for
from psycopg2 import connect
from config import Config

app = Flask(__name__)

# Database connection
def db_connect():
    conn = connect(Config().CONNECTION_STRING)
    return conn

# Define a function to get the election results from the database
def get_election_results(conn):
    with conn.cursor() as cur:
        # Get the total number of votes cast
        cur.execute("SELECT SUM(sport) AS sum_sport, SUM(welfare) AS sum_welfare, SUM(social) AS sum_social, SUM(treasurer) AS sum_treasurer FROM election.results;")
        total_votes = cur.fetchall()[0]
        
        # Get the number of votes for each candidate
        cur.execute("SELECT candidate, COUNT(*) FROM votes GROUP BY candidate")
        vote_results = cur.fetchall()
        
        # Calculate the percentage of votes for each candidate
        vote_percentages = [(candidate, votes / total_votes * 100) for candidate, votes in vote_results]
        
        # Sort the candidates by number of votes
        sorted_results = sorted(vote_percentages, key=lambda x: x[1], reverse=True)
        
        # Get the winner (candidate with the most votes)
        winner = sorted_results[0][0]
        
        return {
            "total_votes": total_votes,
            "vote_results": vote_results,
            "vote_percentages": vote_percentages,
            "sorted_results": sorted_results,
            "winner": winner
        }

# Define a function to check if the election is currently open
def is_election_open(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT value FROM settings WHERE key = 'election_open'")
        return cur.fetchone()[0] == "True"

# Define a route to display the dashboard
@app.route("/dashboard")
def dashboard():
    # Connect to the database
    conn = db_connect()

    # Check if the election is currently open
    election_open = is_election_open(conn)
    
    # Get the election results from the database
    election_results = get_election_results(conn)
    
    # Close the database connection
    conn.close()
    
    # Render the dashboard template with the election results and whether the election is open
    return render_template("dashboard.html", election_results=election_results, election_open=election_open)

# Define a route to close the election
@app.route("/close_election")
def close_election():
    # Connect to the database
    conn = db_connect()

    with conn.cursor() as cur:
        # Update the election_open setting to False
        cur.execute("UPDATE settings SET value = 'False' WHERE key = 'election_open'")
        conn.commit()
    
    # Close the database connection
    conn.close()
    
    # Redirect to the dashboard
    return redirect(url_for("dashboard"))
