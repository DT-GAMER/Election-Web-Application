from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    voter_id = db.Column(db.String(120), unique=True, nullable=False)
    voter_key = db.Column(db.String(120), unique=True, nullable=False)
    voted = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"User('{self.full_name}', '{self.email}', '{self.voter_id}', '{self.voter_key}', '{self.voted}')"

class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    candidates = db.relationship('Candidate', backref='position', lazy=True)

    def __repr__(self):
        return f"Position('{self.name}')"

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'), nullable=False)
    votes = db.Column(db.Integer, default=0, nullable=False)

    def __repr__(self):
        return f"Candidate('{self.full_name}', '{self.position}', '{self.votes}')"

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.String(10), nullable=False)
    candidate_id = db.Column(db.Integer, nullable=False)
    position_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Vote('{self.voter_id}', '{self.candidate_id}', '{self.position_id}')"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
