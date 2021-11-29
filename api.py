import base64
import json

from flask import Blueprint, request

import bakand.cryptography as cp
from bakand.db.dbClasses import User, db, Score
from bakand.utils import getMaps

api = Blueprint('api', __name__, template_folder='templates')


@api.route('/api')
def apiMain():
    return 'this is the API'


@api.route('/api/key', methods=['GET'])
def getKey():
    uid = request.headers.get('Id')
    if uid is None:
        return base64.b64encode('Nope'.encode())
    user = User.query.filter_by(guid=uid).first()
    if user is None:
        return base64.b64encode('No such user'.encode())
    key = cp.genKey(uid.encode())
    data = cp.genPsw()
    print(data)
    user.otp = data
    db.session.commit()
    toSend = cp.encrypt(data, key, uid)

    return base64.b64encode(toSend)


@api.route('/api/upload', methods=['POST'])
def upload():
    uid = request.headers.get('Id')
    if uid is None:
        return base64.b64encode('Nope'.encode())
    user = User.query.filter_by(guid=uid).first()
    if user is None:
        return base64.b64encode('No such user'.encode())
    content = request.json
    decrypted = cp.decrypt(cp.genKey(user.otp.encode()), base64.b64decode(content['data']), uid)
    loaded = json.loads(decrypted.decode())
    error = 0
    print(loaded)
    if loaded['checksum'] != '9360e9de5230b5e1a1c7a79d15f17d0386878cdff9d72df9b4f4768be31b8249':
        error = 1
        print(error)
        return base64.b64encode('Don\'t mess with the jar! ):'.encode())
    user = User.query.filter_by(guid=loaded['player']).first()
    if user is None:
        error = 2
        print(error)
        return base64.b64encode('No such user'.encode())
    maps = getMaps()
    songMap = loaded['map']
    score = songMap['score']
    del songMap['score']
    if songMap not in maps:
        error = 3
        print(error)
        return base64.b64encode('No such map'.encode())
    print(error)
    score = Score(mid=songMap['MID'], title=songMap['title'], artist=songMap['artist'], creator=songMap['creator'],
                  version=songMap['version'], score=score, msid=songMap['MSID'], user_id=user.id)
    db.session.add(score)
    db.session.commit()
    return str(decrypted)
