import random
import string

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def createGuid():
    gid = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(16))
    # TODO: Check that id isn't already in database
    # while len(User.query.filter_by(guid=gid).all()) != 0:
    #     gid = ''.join(
    #         random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(16))
    return gid


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), nullable=False)
    guid = db.Column(db.String(16), nullable=False, default=createGuid())
    accountPassword = db.Column(db.String(45), nullable=False)
    otp = db.Column(db.String(20))

    def __repr__(self):
        return 'User: ' + self.username + ' GUID: ' + self.guid
