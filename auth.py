import psycopg2
import config


def authenticate(login_key):
    """Authenticate the user with the given login key."""
    try:
        # Connect to the database
        conn = psycopg2.connect(config.self.CONNECTION_STRING)
        cur = conn.cursor()

        # Check if the login key is valid
        cur.execute("SELECT full_name FROM users WHERE login_key = %s", (login_key,))
        result = cur.fetchone()
        if result is None:
            return None

        # Return the user's full name
        return result[0]

    except Exception as e:
        print(f"Error authenticating user with login key {login_key}: {e}")
        return None

    finally:
        # Close the database connection
        cur.close()
        conn.close()
