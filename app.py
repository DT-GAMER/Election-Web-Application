from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime
from config import Config
import register
import login
import vote
import dashboard
import psycopg2
import uuid
import smtplib
import ssl
import os

app = Flask(__name__)
CORS(app)
app.config.from_object(config.Config())
app.config['CORS_HEADERS'] = 'Content-Type'

# Database connection
def connect():
    conn = psycopg2.connect(Config().CONNECTION_STRING)
    return conn

# Register endpoint
@app.route('/register', methods=['GET', 'POST'])
@cross_origin()
def register_user():
    if request.method == 'POST':
        conn = connect()
        cur = conn.cursor()
        data = request.get_json()
        email = data['email']
        full_name = data['full_name']
        key = str(uuid.uuid4())[:24] # Generate unique 24-char key
        now = datetime.now()
        create_date = now.strftime("%Y-%m-%d %H:%M:%S")
        sql = """INSERT INTO users (email, full_name, login_key, create_date) VALUES (%s, %s, %s, %s)"""
        cur.execute(sql, (email, full_name, key, create_date))
        conn.commit()
        conn.close()

        # Send key to user's email
        sender_email = "theelectoralcollege24@gmail.com"
        sender_password = "electoralcollege2023"
        receiver_email = email
        message = f"""\
        Subject: Your Election Login Key
        
        Your login key for the election is: {key}
        
        You can use this key to login at any time between 8am and 12 noon on the day of the election.
        
        Thank you for participating in the election."""

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message)

        return jsonify({'message': 'Registration successful. Login key has been sent to your email.'})
    else:
        return jsonify({'message': 'Invalid request method.'}), 405

# Login endpoint
@app.route('/login', methods=['GET', 'POST'])
@cross_origin()
def login_user():
    if request.method == 'POST':
        conn = connect()
        cur = conn.cursor()
        data = request.get_json()
        login_key = data['login_key']
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        if current_time < "08:00:00" or current_time > "12:00:00":
            return jsonify({'message': 'Voting is only allowed between 8am and 12 noon on the day of the election.'}), 403
        cur.execute("SELECT * FROM users WHERE login_key=%s", (login_key,))
        user = cur.fetchone()
        conn.close()
        if user:
            return jsonify({'message': 'Login successful.'})
        else:
            return jsonify({'message': 'Invalid login key.'}), 401
    else:
        return jsonify({'message': 'Invalid request method.'}), 405



# Vote endpoint
@app.route('/vote', methods=['POST'])
@cross_origin()
@jwt_required
def vote_user():
    # get the user's vote choice from the request body
    data = request.get_json()
    vote_choice = data['vote_choice']

    # validate the vote choice
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM candidates WHERE id=%s", (vote_choice,))
    candidate_exists = cur.fetchone()[0]
    conn.close()

    if not candidate_exists:
        return jsonify({'message': 'Invalid vote choice.'}), 400

    # get the user's ID from the token
    user_id = get_jwt_identity()

    # check if the user has already voted
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT vote_time FROM votes WHERE user_id=%s", (user_id,))
    vote_time = cur.fetchone()
    conn.close()

    if vote_time is not None:
        return jsonify({'message': 'User has already voted.'}), 400

    # record the user's vote in the database
    conn = connect()
    cur = conn.cursor()
    now = datetime.now()
    vote_time = now.strftime("%Y-%m-%d %H:%M:%S")
    sql = """INSERT INTO votes (user_id, candidate_id, vote_time) VALUES (%s, %s, %s)"""
    cur.execute(sql, (user_id, vote_choice, vote_time))
    conn.commit()
    conn.close()

    # get the current vote count for each candidate
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT candidates.id, candidates.name, COUNT(votes.id) FROM candidates LEFT JOIN votes ON candidates.id=votes.candidate_id GROUP BY candidates.id ORDER BY COUNT(votes.id) DESC")
    results = cur.fetchall()
    conn.close()

    # return the vote count for each candidate
    return jsonify({'message': 'Vote successful.', 'results': results})

@app.route('/dashboard')
def dashboard_result():
    conn = connect()
    cur = conn.cursor()

    # Get the total number of votes cast
    cur.execute("SELECT COUNT(*) FROM votes")
    total_votes = cur.fetchone()[0]

    # Get the total number of votes for each candidate
    cur.execute("SELECT candidate_id, COUNT(*) FROM votes GROUP BY candidate_id")
    candidate_votes = dict(cur.fetchall())

    # Get the name of each candidate
    cur.execute("SELECT id, name FROM candidates")
    candidates = dict(cur.fetchall())

    # Format the data
    results = []
    for candidate_id, vote_count in candidate_votes.items():
        candidate_name = candidates[candidate_id]
        vote_percentage = (vote_count / total_votes) * 100
        results.append({
            'candidate_name': candidate_name,
            'vote_count': vote_count,
            'vote_percentage': vote_percentage
        })

    # Sort the results by vote count in descending order
    results.sort(key=lambda x: x['vote_count'], reverse=True)

    # Close the database connection
    conn.close()

    # Return the results as a JSON response
    return jsonify({
        'total_votes': total_votes,
        'results': results
    })


@app.route('/')
def application_great():
    return 'This application is great!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

