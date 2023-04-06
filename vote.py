import psycopg2
from datetime import datetime
from config import Config


def vote(candidate_id, voter_id):
    """Cast a vote for the specified candidate by the given voter."""
    
    # Connect to the database
    conn = psycopg2.connect(config.CONNECTION_STRING)
    
    try:
        # Begin a transaction
        with conn.cursor() as cur:
            
            # Check if the voter has already voted
            cur.execute("SELECT * FROM election.results WHERE voters_id = %s", (voter_id,))
            result = cur.fetchone()
            if result is not None:
                raise Exception("This voter has already cast a vote.")
            
            # Insert the vote into the database
            voted_at = datetime.now()
            cur.execute("INSERT INTO election.results (voters_id, sport, welfare, social, treasurer) VALUES (%s, %s, %s, %s, %s)", 
                        (voter_id, sport, welfare, social, treasurer))
            
            # Commit the transaction
            conn.commit()
    
    except Exception as e:
        # Rollback the transaction if there was an error
        conn.rollback()
        raise e
    
    finally:
        # Close the database connection
        conn.close()
