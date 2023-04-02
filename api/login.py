import psycopg2

conn = psycopg2.connect(database="election", user="postgres", password="password", host="127.0.0.1", port="5432")
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
