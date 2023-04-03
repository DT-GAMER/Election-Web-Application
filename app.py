from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from api.register import register_user
from api.login import login_user
from api.vote import vote_candidate
from api.dashboard import get_results
import psycopg2
import uuid
import smtplib
import ssl
import os

start_app = Flask(__name__)
CORS(start_app)

# Database connection
def connect():
    conn = psycopg2.connect(
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn

# Register endpoint
@app.route('/register', methods=['GET', 'POST'])
def register():
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
def login():
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
def vote():
    # get the user's vote choice from the request body
    data = request.get_json()
    vote_choice = data['vote_choice']

    # get the user's token from the request headers
    token = request.headers.get('Authorization')

    # check if the token exists in the database
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE login_key=%s", (token,))
    user = cur.fetchone()
    conn.close()

    if user is None:
        return jsonify({'message': 'Invalid token'}), 401

    # check if the user has already voted
    if user[4] is not None:
        return jsonify({'message': 'User has already voted'}), 400

    # record the user's vote in the database
    conn = connect()
    cur = conn.cursor()
    now = datetime.now()
    vote_time = now.strftime("%Y-%m-%d %H:%M:%S")
    sql = """INSERT INTO votes (user_id, candidate_id, vote_time) VALUES (%s, %s, %s)"""
    cur.execute(sql, (user[0], vote_choice, vote_time))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Vote successful'})


@app.route('/dashboard')
def dashboard():
    result = get_results()
    return jsonify(result)

@app.route('/')
def application_great():
    return 'This application is great!'

if __name__ == 'main':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

