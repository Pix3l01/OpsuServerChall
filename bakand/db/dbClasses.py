from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

import bakand.cryptography as cp

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), nullable=False)
    guid = db.Column(db.String(16), nullable=False)
    password = db.Column(db.String(45), nullable=False)
    otp = db.Column(db.String(20))

    def __repr__(self):
        return 'User: ' + self.username + ' GUID: ' + self.guid
