import psycopg2
from psycopg2  import Error
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

"""Creating that Database that would accept User's info.
Such information would be used to create a users profile 
as well as log in details.
"""
# Function to create Database & Table using PostGreSQL
def accounts():
    global conn, cursor
    try:
        conn = psycopg2.connect(user=DB_USER,
                                password=DB_PASSWORD,
                                host=DB_HOST,
                                port=DB_PORT,
                                database=DB_NAME)
        # Creating cursor to perform DB Opertions
        cursor = conn.cursor()
        # SQL query to create a table
        create_table = """CREATE TABLE SignUp 
        (ID INT GENERATED ALWAYS AS IDENTITY ,Email TEXT NOT NULL PRIMARY KEY,Names TEXT NOT NULL, 
        Password TEXT NOT NULL)"""
        # Execute Command: creates table SignUp
        cursor.execute(create_table)
        conn.commit()
        print("Table Created Succesfully in DB")
    except(Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if conn:
            cursor.close()
            conn.close()

accounts()