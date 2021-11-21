import base64

from flask import Flask, render_template, request
from Crypto import Random

import bakand.cryptography as cp

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api')
def api():
    return 'this is the API'


@app.route('/api/key', methods=['GET'])
def getKey():
    uid = request.headers.get('Id')
    if uid is None:
        return base64.b64encode('Nope'.encode())
    key = cp.genKey(uid.encode())
    data = cp.genPsw()
    print(data)
    cp.chiavissima = data
    toSend = cp.encrypt(data, key, uid)

    return base64.b64encode(toSend)


@app.route('/api/upload', methods=['POST'])
def upload():
    uid = request.headers.get('Id')
    if uid is None:
        return base64.b64encode('Nope'.encode())
    content = request.json
    decrypted = cp.decrypt(cp.genKey(cp.chiavissima.encode()), base64.b64decode(content['data']), uid)
    print(decrypted)
    return str(decrypted)


if __name__ == '__main__':
    app.run()
