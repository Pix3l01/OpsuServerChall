import base64
import json
import time

from flask import Blueprint, request

import bakand.cryptography as cp
from bakand.db.dbClasses import User, db, Score
from bakand.utils import getMaps, getClientHash

api = Blueprint('api', __name__, template_folder='templates')
clientHash, last = getClientHash()


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
    global clientHash, last
    if uid is None:
        return base64.b64encode('Nope'.encode())
    user = User.query.filter_by(guid=uid).first()
    if user is None:
        return base64.b64encode('No such user'.encode())
    if user.otp is '' or user.otp is None:
        print(user.otp)
        return base64.b64encode('Something went wrong storing the key. Please ask for another'.encode())
    try:
        content = request.json
        decrypted = cp.decrypt(cp.genKey(user.otp.encode()), base64.b64decode(content['data']), uid)
        loaded = json.loads(decrypted.decode())
        error = 0
        print(loaded)
        if time.time() - last > 60:
            clientHash, last = getClientHash()
        if loaded['checksum'] != clientHash:
            error = 1
            print(error)
            return base64.b64encode('Don\'t mess with the jar! @:<'.encode())
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
    except Exception as e:
        print(e)
    user.otp = ''
    db.session.commit()
    return str(decrypted)
