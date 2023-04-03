import psycopg2
from psycopg2 import Error
from config import USERNAME, PASSWORD, DATABASE_HOST, DATABASE_PORT, DATABASE_NAME

"""Creating that Database that would accept User's info.
Such information would be used to create a users profile 
as well as log in details.
"""
# Function to create Schema using PostGreSQL
def Schema():
    try:
        conn = psycopg2.connect(user=USERNAME,
                                password=PASSWORD,
                                host=DATABASE_HOST,
                                port=DATABASE_PORT,
                                database=DATABASE_NAME)
        # Creating cursor to perform DB Opertions
        cursor = conn.cursor()
        # SQL query to create a table
        create_schema = """CREATE SCHEMA Election"""
        # Execute Command: creates table SignUp
        cursor.execute(create_schema)
        conn.commit()
        print("Table Created Succesfully in ElectionDB")
    except(Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if conn:
            cursor.close()
            conn.close()

# Function to create Database & Table using PostGreSQL
def accountTable():
    try:
        conn = psycopg2.connect(user=USERNAME,
                                password=PASSWORD,
                                host=DATABASE_HOST,
                                port=DATABASE_PORT,
                                database=DATABASE_NAME)
        # Creating cursor to perform DB Opertions
        cursor = conn.cursor()
        # SQL query to create a table
        create_table = """CREATE TABLE Election.SignUp 
        (ID INT GENERATED ALWAYS AS IDENTITY ,Email TEXT NOT NULL PRIMARY KEY,Names TEXT NOT NULL, 
        Key TEXT NOT NULL)"""
        # Execute Command: creates table SignUp
        cursor.execute(create_table)
        # Adding unique constraint to ID column
        cursor.execute("""ALTER TABLE Election.SignUp ADD CONSTRAINT uniq_signup_id UNIQUE (ID);""")
        conn.commit()
        print("Table Created Succesfully in ElectionDB")
    except(Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if conn:
            cursor.close()
            conn.close()


""" This codes below create candidates table for 
the contestants and add them as well as result table that stores 
each voters votes."""

def Positions():
    try:
        conn = psycopg2.connect(user=USERNAME,
                                password=PASSWORD,
                                host=DATABASE_HOST,
                                port=DATABASE_PORT,
                                database=DATABASE_NAME)
        cursor = conn.cursor()
        createTable = """ CREATE TABLE ELECTION.Positions
                (ID SERIAL PRIMARY KEY,
                Position TEXT NOT NULL,
                CONSTRAINT uk_ID UNIQUE (ID))"""
        cursor.execute(createTable)
        conn.commit()
        print("Table Created Succesfully in ElectionDB")
    except(Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if conn:
            cursor.close()
            conn.close()

# Function to create Database & Table using PostGreSQL
def candidates():
    try:
        conn = psycopg2.connect(user=USERNAME,
                                password=PASSWORD,
                                host=DATABASE_HOST,
                                port=DATABASE_PORT,
                                database=DATABASE_NAME)
        cursor = conn.cursor()
        createTable = """CREATE TABLE ELECTION.CANDIDATES
        (ID SERIAL PRIMARY KEY, Candidates TEXT NOT NULL, 
        Pos_ID INT REFERENCES ELECTION.POSITIONS(ID))"""
        cursor.execute(createTable)
        conn.commit()
        print("Table Created Succesfully in ElectionDB")
    except(Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if conn:
            cursor.close()
            conn.close()



def resultCounts():
    try:
        conn = psycopg2.connect(user=USERNAME,
                                password=PASSWORD,
                                host=DATABASE_HOST,
                                port=DATABASE_PORT,
                                database=DATABASE_NAME)
        cursor = conn.cursor()
        createTable = """CREATE TABLE ELECTION.RESULTS (
            Id SERIAL PRIMARY KEY,
            Voters_ID INT,
            Sport INT NOT NULL,
            Welfare INT NOT NULL,
            Social INT NOT NULL,
            Treasurer INT NOT NULL,
            CONSTRAINT fk_voters_id FOREIGN KEY (Voters_ID) REFERENCES ELECTION.SignUp(ID),
            CONSTRAINT fk_sport_pos_id FOREIGN KEY (Sport) REFERENCES ELECTION.Candidates(id),
            CONSTRAINT fk_welfare_pos_id FOREIGN KEY (Welfare) REFERENCES ELECTION.Candidates(id),
            CONSTRAINT fk_social_cand_id FOREIGN KEY (Social) REFERENCES ELECTION.Candidates(id),
            CONSTRAINT fk_treasurer_cand_id FOREIGN KEY (Treasurer) REFERENCES ELECTION.Candidates(id),
            CONSTRAINT chk_sport_id CHECK (Sport IN (5,7,11)),
            CONSTRAINT chk_welfare_id CHECK (Welfare IN(6,8)),
            CONSTRAINT chk_social_id CHECK (Social IN (1,2,10)),
            CONSTRAINT chk_treasurer_id CHECK (Treasurer IN (12,13))
        );"""
        cursor.execute(createTable)
        conn.commit()
        print("Table Created Successfully in ElectionDB")
    except(Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if conn:
            cursor.close()
            conn.close()


