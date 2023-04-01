import psycopg2
from psycopg2 import Error

def add_candidates(Names, Position):
    try:
        conn = psycopg2.connect(user="postgres",
                                password="k0r0.day",
                                host="localhost",
                                port="5432",
                                database="electiondb")
        cursor = conn.cursor()
        addContestants = """ INSERT INTO Election.CANDIDATES(Candidates,Pos_ID) VALUES(%s,%s)"""
        values = (Names, Position)
        cursor.execute(addContestants,values)
        conn.commit()
        print("Data Inserted Succesfully!")
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if conn:
            cursor.close()
            conn.close()


def addPositions(Position ):
    try:
        conn = psycopg2.connect(user="postgres",
                                password="k0r0.day",
                                host="localhost",
                                port="5432",
                                database="electiondb")
        cursor = conn.cursor()
        addContestants = """ INSERT INTO Election.Positions(Position) VALUES(%s)"""
        values = (Position,)
        cursor.execute(addContestants, values)
        conn.commit()
        print("Data Inserted Succesfully!")
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if conn:
            cursor.close()
            conn.close()


input()
addPositions("GENERAL SECRETARY")
addPositions("ASSISTANT GENERAL SECRETARY")
addPositions("SOCIAL SECRETARY")
addPositions("WELFARE SECRETARY")
addPositions("FINANCIAL SECRETARY")
addPositions("SPORT SECRETARY")
addPositions("TREASURER")
addPositions("PUBLIC RELATIONS OFFICER")


"Passing Candidates information into the Table"
add_candidates("SHONEYE OMOLOLA SERAH", 3)
add_candidates("AKINTUNDE ITUNUOLUWAPO ANJOLAOLUWA", 3)
add_candidates("ANNAUN SAMUEL", 8)
add_candidates("MUOGHALU CHINYERE LOVE", 5)
add_candidates("FARINLOYE FOLAKE SUSAN", 6)
add_candidates("OLOMOLA VICTORIA AYOMIDE", 4)
add_candidates("ALLI-KAMAL MAZEEDAH OYINDAMOLA", 6)
add_candidates("YUSUF AMINAT OPEYEMI", 4)
add_candidates("OYEYINKA OLUWAPELUMI SARAH", 2)
add_candidates("AKINYOMI SEFUNMI ISAIAH", 3)
add_candidates("BABALOLA AYOOLA SAMUEL", 6)
add_candidates("TAIWO ELIZABETH FOWODE", 7)