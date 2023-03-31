import psycopg2
from psycopg2 import Error
import bcrypt
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

"""Encryption Salt would be used to encrypt passwords during SignUp"""
salt = bcrypt.gensalt()

"""This function enables user defined data to be passed into.
the SIGNUP_TABLE on the database
"""
def add_into_DB(Email, Names, Password):
    try:
        psycopg2.connect(user=DB_USER,
                         password=PASSWORD,
                         host=DB_HOST,
                         port=DB_PORT,
                         database=DB_NAME)
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    conn = psycopg2.connect(user="postgres",
                         password="k0r0.day",
                         host="localhost",
                         port="5432",
                         database="accounts")
    c = conn.cursor()
    try:
        insert = "INSERT INTO SignUp(Email, Names, Password) VALUES (%s,%s,%s)"
        values = (Email, Names, encrypt(Password))
        c.execute(insert,values)
        print("Data Inserted")
    except psycopg2.IntegrityError:
        print("This user already exists. Try logging in instead")
    conn.commit()
    conn.close()

""" Encryption & Decryption Functions for Passwords """
def encrypt(Password):
    return bcrypt.hashpw(Password.encode(), salt).decode()

def decrypt(Password, hashed):
    return bcrypt.checkpw(Password.encode(), hashed)


"""Function for Login"""
def Login():
    """ This accepts users Email input and checks for it in the DB
    A non existent account would be referred to sign up, while an existent
    account would proceed to password"""

    # DBO Email Check
    try:
        Email = input("Email: ")
        conn = psycopg2.connect(user="postgres",
                         password="k0r0.day",
                         host="localhost",
                         port="5432",
                         database="accounts")
        c = conn.cursor()
        retrieve = "SELECT Email FROM SignUp WHERE Email = '{0}'".format(Email)
        c.execute(retrieve)
        mail = c.fetchone()
        conn.close()
        if mail is not None:
            pass
        else:
            raise ValueError("This Account doesn't exist, Sign up instead")
    except ValueError as e:
        print(e)

    # Password
    try:
        Password = input("Password: ")
        conn = psycopg2.connect(user="postgres",
                                password="k0r0.day",
                                host="localhost",
                                port="5432",
                                database="accounts")
        c = conn.cursor()
        retrieve = "SELECT Password FROM SignUp WHERE Email = '{0}'".format(Email)
        c.execute(retrieve)
        iterable = c.fetchall()
        if iterable:
            hashed_pwd = iterable[0][0].encode('utf-8')
            if decrypt(Password, hashed_pwd):
                print("Login Successful!")
            else:
                raise Exception("Incorrect Password! Try again")
        else:
            raise ValueError("This Account doesn't exist, Sign up instead")
    except (Exception, Error) as e:
        print(e)

Login()
