from enum import unique
from app import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLalchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    votes = db.relationship('Vote', backref='voter', lazy=True)

    def __repr__(self):
        return f"User('{self.full_name}', '{self.email}')"


class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    position = db.Column(db.String(120), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    votes = db.relationship('Vote', backref='candidate', lazy=True)

    def __repr__(self):
        return f"Candidate('{self.name}', '{self.position}')"


class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
    position = db.Column(db.String(120), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Vote('{self.position}', '{self.date_posted}')"   
