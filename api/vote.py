import psycopg2
from datetime import datetime

# Database connection parameters
host = "localhost"
database = "election"
user = "postgres"
password = "your_password"

def vote(candidate_id, voter_id):
    """Cast a vote for the specified candidate by the given voter."""
    
    # Connect to the database
    conn = psycopg2.connect(host=host, database=database, user=user, password=password)
    
    try:
        # Begin a transaction
        with conn.cursor() as cur:
            
            # Check if the voter has already voted
            cur.execute("SELECT voted_at FROM votes WHERE voter_id = %s", (voter_id,))
            result = cur.fetchone()
            if result is not None:
                raise Exception("This voter has already cast a vote.")
            
            # Insert the vote into the database
            voted_at = datetime.now()
            cur.execute("INSERT INTO votes (candidate_id, voter_id, voted_at) VALUES (%s, %s, %s)", 
                        (candidate_id, voter_id, voted_at))
            
            # Commit the transaction
            conn.commit()
    
    except Exception as e:
        # Rollback the transaction if there was an error
        conn.rollback()
        raise e
    
    finally:
        # Close the database connection
        conn.close()
