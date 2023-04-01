import unittest
from app import create_app, db
from models import User, Candidate, Position

class TestModels(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create test user
        self.user = User(username='testuser', voter_id='123', voter_key='abc')
        db.session.add(self.user)

        # Create test positions
        self.pos1 = Position(name='President')
        self.pos2 = Position(name='Vice President')
        db.session.add_all([self.pos1, self.pos2])

        # Create test candidates
        self.cand1 = Candidate(name='John Doe', position=self.pos1)
        self.cand2 = Candidate(name='Jane Smith', position=self.pos2)
        db.session.add_all([self.cand1, self.cand2])

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_creation(self):
        # Test user creation
        user = User(username='newuser', voter_id='456', voter_key='def')
        db.session.add(user)
        db.session.commit()

        assert user.id is not None
        assert user.username == 'newuser'
        assert user.voter_id == '456'
        assert user.voter_key == 'def'

    def test_position_creation(self):
        # Test position creation
        pos = Position(name='Secretary')
        db.session.add(pos)
        db.session.commit()

        assert pos.id is not None
        assert pos.name == 'Secretary'

    def test_candidate_creation(self):
        # Test candidate creation
        cand = Candidate(name='Bob Johnson', position=self.pos1)
        db.session.add(cand)
        db.session.commit()

        assert cand.id is not None
        assert cand.name == 'Bob Johnson'
        assert cand.position == self.pos1

    def test_get_user_by_voter_id(self):
        # Test getting user by voter ID
        user = User.query.filter_by(voter_id='123').first()

        assert user is not None
        assert user.username == 'testuser'
        assert user.voter_id == '123'
        assert user.voter_key == 'abc'

    def test_get_candidate_by_position(self):
        # Test getting candidates by position
        candidates = Candidate.query.filter_by(position=self.pos1).all()

        assert len(candidates) == 1
        assert candidates[0].name == 'John Doe'
        assert candidates[0].position == self.pos1

if __name__ == '__main__':
    unittest.main()
