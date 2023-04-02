from app import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    login_key = db.Column(db.String(24), unique=True, nullable=False)
    has_voted = db.Column(db.Boolean, default=False)
    vote_choice = db.Column(db.String(50))

    def __repr__(self):
        return '<User {}>'.format(self.email)


class Candidate(db.Model):
    __tablename__ = 'candidates'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    votes = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Candidate {}>'.format(self.name)
