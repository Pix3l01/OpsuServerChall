import base64

from flask import Blueprint, request

import bakand.cryptography as cp
from bakand.db.dbClasses import User, db

api = Blueprint('api', __name__, template_folder='templates')


@api.route('/api')
def apiMain():
    return 'this is the API' + str(User.query.all())


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
    cp.chiavissima = data
    toSend = cp.encrypt(data, key, uid)

    return base64.b64encode(toSend)


@api.route('/api/upload', methods=['POST'])
def upload():
    uid = request.headers.get('Id')
    if uid is None:
        return base64.b64encode('Nope'.encode())
    content = request.json
    decrypted = cp.decrypt(cp.genKey(cp.chiavissima.encode()), base64.b64decode(content['data']), uid)
    print(decrypted)
    return str(decrypted)