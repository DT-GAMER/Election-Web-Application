import psycopg2
from psycopg2 import Error
import bcrypt
import random
import string
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

"""Encryption Salt would be used to encrypt passwords during SignUp"""
salt = bcrypt.gensalt()

"""This function enables user defined data to be passed into.
the SIGNUP_TABLE on the database
"""


def add_into_DB(Email, Names):
    try:
        conn = psycopg2.connect(user=DB_USER,
                                password=DB_PASSWORD,
                                host=DB_HOST,
                                port=DB_PORT,
                                database=DB_NAME)
        c = conn.cursor()
        key = Key()
        insert = "INSERT INTO Election.SignUp(Email, Names, Key) VALUES (%s,%s,%s)"
        values = (Email.upper(), Names.upper(), key)
        c.execute(insert, values)
        print("Data Inserted")
        retrieve = "SELECT ID FROM ELECTION.Signup WHERE EMAIL = '{}';".format(Email)
        c.execute(retrieve)
        conn.commit()
        print("Your 24 character long Voters Key: " + key + "\nSave carefully for future use.")
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (conn):
            c.close()
            conn.close()
            print("PostgreSQL connection is closed")


""" Upon registration, a key is generated for the user, 
which will serve as the entry key to the portal. This is subject to request. The function key generates the key for the user"""

def Key():
    # Define the set of printable characters including hyphens
    chars = string.ascii_letters + string.digits
    # Generate a 24-character key using the valid characters
    key = ''.join(random.choice(chars) for _ in range(24))
    return (key)

"""Function for Login"""
def Login():
    """ This accepts users Key input and checks for it in the DB
    A non existent Key would not be allowed access, while an existent
    key would proceed to Dashboard"""

    try:
        conn = psycopg2.connect(user=DB_USER,
                                password=DB_PASSWORD,
                                host=DB_HOST,
                                port=DB_PORT,
                                database=DB_NAME)
        c = conn.cursor()
        key = input("Key: ")
        retrieve = "SELECT key FROM Election.SignUp WHERE key = %s"
        c.execute(retrieve, (key,))
        retrievedkey = c.fetchone()
        if retrievedkey and key == retrievedkey[0]:
            print("Login Successful!")
        else:
            raise Exception("Incorrect Key! Try again")
    except (Exception, Error) as e:
        print(e)
    finally:
        if (conn):
            c.close()
            conn.close()
            print("PostgreSQL connection is closed")



Login()