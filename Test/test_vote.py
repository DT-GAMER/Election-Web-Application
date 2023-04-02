import unittest
import psycopg2
from datetime import datetime
from unittest.mock import patch, MagicMock

import vote

class TestVote(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.conn = psycopg2.connect(database="test_election", user="postgres", password="password", host="127.0.0.1", port="5432")
        
        with cls.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS candidates (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS voters (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS votes (
                    id SERIAL PRIMARY KEY,
                    candidate_id INTEGER NOT NULL,
                    voter_id INTEGER NOT NULL,
                    voted_at TIMESTAMP NOT NULL,
                    FOREIGN KEY (candidate_id) REFERENCES candidates (id),
                    FOREIGN KEY (voter_id) REFERENCES voters (id)
                );
            """)
            cls.conn.commit()
            
            cur.execute("""
                INSERT INTO candidates (name) VALUES
                ('Candidate 1'),
                ('Candidate 2');
            """)
            cls.candidate_id = cur.fetchone()[0]
            
            cur.execute("""
                INSERT INTO voters (name) VALUES
                ('Voter 1');
            """)
            cls.voter_id = cur.fetchone()[0]
    
    def setUp(self):
        self.conn = self.__class__.conn
        
    def test_vote_success(self):
        with self.conn.cursor() as cur:
            vote.vote(self.__class__.candidate_id, self.__class__.voter_id)
            
            cur.execute("""
                SELECT * FROM votes WHERE candidate_id = %s AND voter_id = %s;
            """, (self.__class__.candidate_id, self.__class__.voter_id))
            result = cur.fetchone()
            
            self.assertIsNotNone(result)
            self.assertIsInstance(result[0], int)
            self.assertEqual(result[1], self.__class__.candidate_id)
            self.assertEqual(result[2], self.__class__.voter_id)
            self.assertIsInstance(result[3], datetime)
    
    def test_duplicate_vote(self):
        with self.conn.cursor() as cur:
            vote.vote(self.__class__.candidate_id, self.__class__.voter_id)
            
            with self.assertRaises(Exception):
                vote.vote(self.__class__.candidate_id, self.__class__.voter_id)
            
            cur.execute("""
                SELECT COUNT(*) FROM votes WHERE candidate_id = %s;
            """, (self.__class__.candidate_id,))
            count = cur.fetchone()[0]
            
            self.assertEqual(count, 1)
    
    @classmethod
    def tearDownClass(cls):
        with cls.conn.cursor() as cur:
            cur.execute("""
                DROP TABLE IF EXISTS votes;
            """)
            cur.execute("""
                DROP TABLE IF EXISTS candidates;
            """)
            cur.execute("""
                DROP TABLE IF EXISTS voters;
            """)
            cls.conn.commit()
            
        cls.conn.close()

if __name__ == '__main__':
    unittest.main()
