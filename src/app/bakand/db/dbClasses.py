from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

import bakand.cryptography as cp

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), nullable=False)
    guid = db.Column(db.String(16), nullable=False, unique=True)
    password = db.Column(db.String(45), nullable=False)
    otp = db.Column(db.String(20))
    scores = db.relationship('Score')

    def __repr__(self):
        return 'User: ' + self.username + ' GUID: ' + self.guid


class Score(db.Model):
    __tablename__ = 'scores'
    id = db.Column(db.Integer, primary_key=True)
    mid = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(45), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    creator = db.Column(db.String(100), nullable=False)
    version = db.Column(db.String(45), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    msid = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return 'Map id: ' + str(self.mid) + ' - Score: ' + str(self.score)
