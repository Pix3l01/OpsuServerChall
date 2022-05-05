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
    user.otp = data
    db.session.commit()
    toSend = cp.encrypt(data, key, uid)
    print(f'{user.username} : {uid} has requested a key', flush=True)

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
    if user.otp == '' or user.otp is None:
        print(f'{user.username} : {uid} key was missing from the db', flush=True)
        return base64.b64encode('Something went wrong storing the key. Please ask for another'.encode())
    try:
        content = request.json
        decrypted = cp.decrypt(cp.genKey(user.otp.encode()), base64.b64decode(content['data']), uid)
        loaded = json.loads(decrypted.decode())
        error = False
        if time.time() - last > 60:
            clientHash, last = getClientHash()
        if loaded['checksum'].lower() != clientHash.lower():
            error = True
            print(f'{user.username} : {uid} checksum mismatch.\nUploaded: {loaded["checksum"].lower()}'
                  f'\nActual:{clientHash.lower()}', flush=True)
            return base64.b64encode('Don\'t mess with the jar! @:<'.encode())
        user = User.query.filter_by(guid=loaded['player']).first()
        if user is None:
            error = True
            print(f'Uid in header ({uid}) and Uid in json ({loaded["player"]}) mismatch', flush=True)
            return base64.b64encode('No such user'.encode())
        maps = getMaps()
        songMap = loaded['map']
        score = songMap['score']
        del songMap['score']
        if songMap not in maps:
            error = True
            print(f'Song uploaded ({songMap}) by {user.username} : {uid} is not part of challenge', flush=True)
            return base64.b64encode('No such map'.encode())
        score = Score(mid=songMap['MID'], title=songMap['title'], artist=songMap['artist'], creator=songMap['creator'],
                      version=songMap['version'], score=score, msid=songMap['MSID'], user_id=user.id)
        db.session.add(score)
        user.otp = ''
        db.session.commit()
        if not error:
            print(f'Score correctly uploaded by {user.username} : {uid}\n{score}', flush=True)
        return base64.b64encode('Score correctly uploaded'.encode())
    except Exception as e:
        print('Unforeseen error occurred', flush=True)
        print(e, flush=True)
    user.otp = ''
    db.session.commit()
    return base64.b64encode('Maybe something went wrong. IDK ¯\\_(ツ)_/¯'.encode())
