import psycopg2
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config



# SMTP email server parameters
SMTP_SERVER = Config.Smpt.SMTP_SERVER
SMTP_PORT = Config.Smpt.SMTP_PORT
EMAIL_ADDRESS = "theelectoralcollege24@gmail.com"
EMAIL_PASSWORD = "electoralcollege2023"


def generate_key(length=24):
    """Generate a random key of a given length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def send_registration_email(email, key):
    """Send a registration email with the given key to the given email address."""
    message = MIMEMultipart()
    message['From'] = EMAIL_ADDRESS
    message['To'] = email
    message['Subject'] = 'Your Election Registration Key'

    body = f'Hello,\n\nYour registration key is: {key}\n\nPlease use this key to login to the election system.'
    message.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, email, message.as_string())


def register_user(full_name, email):
    """Register a new user with the given full name and email address."""
    key = generate_key()

    try:
        # Connect to the database
        conn = psycopg2.connect(config.CONNECTION_STRING)
        cur = conn.cursor()

        # Insert the new user into the database
        cur.execute("INSERT INTO users (full_name, email, login_key) VALUES (%s, %s, %s)", (full_name, email, key))
        conn.commit()

        # Send the registration email to the user
        send_registration_email(email, key)

        print(f"Successfully registered user {full_name} with email {email}")
    except Exception as e:
        print(f"Error registering user {full_name} with email {email}: {e}")
    finally:
        # Close the database connection
        cur.close()
        conn.close()
