import psycopg2
from psycopg2 import Error
from config import USERNAME, PASSWORD, DATABASE_HOST, DATABASE_PORT, DATABASE_NAME
conn = psycopg2.connect(user=USERNAME,
                        password=PASSWORD,
                        host=DATABASE_HOST,
                        port=DATABASE_PORT,
                        database=DATABASE_NAME)
print("Database connected successfully")

def login(key):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE key = %s", (key,))
        user = cur.fetchone()
        if user:
            print("Login successful")
            return True
        else:
            print("Invalid key. Please try again.")
            return False
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        if conn:
            conn.close()
            print("Database connection closed.")
