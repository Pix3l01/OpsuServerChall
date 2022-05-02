import json

import requests
import base64
from hashlib import pbkdf2_hmac
from Crypto.Cipher import AES

BS = 16

def unpad(s):
    return s[0:-s[-1]]

def pad(s):
    return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)


def genKey(password):
    key = pbkdf2_hmac(
        hash_name='sha256',
        password=password,
        salt=b"pwnthem0le",
        iterations=65536,
        dklen=32
    )
    return key


def decrypt(key, enc, user):
    iv = user.encode()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc))

def encrypt(data, key, user):
    iv = user.encode()
    data = pad(data)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(data.encode())


def getKey(url, header):
    data = base64.b64decode(requests.get(url + '/api/key', headers=header).text)
    plain = decrypt(genKey(uid.encode()), data, uid)
    return plain


def upload(url, header, body, hash, key, uid):
    toSend = {'checksum': hash, 'map': body, 'player': uid}
    toSend = base64.b64encode(encrypt(str(json.dumps(toSend)), genKey(key), uid))
    res = requests.post(url+'/api/upload', headers=header, json={'data': toSend.decode()}).text
    print(res)


if __name__ == '__main__':

    # SETUP
    maps = json.loads("""{
  "map1": {
    "MID": 196716,
    "title": "You Suffer",
    "artist": "Napalm Death",
    "creator": "MillhioreF",
    "version": "Easy",
    "MSID": 67814,
    "score": 1501
  },
  "map2": {
    "MID": 87431,
    "title": "FREEDOM DiVE",
    "artist": "xi",
    "creator": "Nakagawa-Kanon",
    "version": "FOUR DIMENSIONS",
    "MSID": 39804,
    "score": 132408003
  },
  "map3": {
    "MID": 31337,
    "title": "Skype x Can Can",
    "artist": "Ara Potato",
    "creator": "Real",
    "version": "Hard",
    "MSID": 47078,
    "score": 3133773314
  }
}""")
    uid = input('Give me your uid: ')
    header = {'Id': uid}
    BASE_URL = input('Give me the base URL: ')
    clientHash = input('Input the sha256 of Client.jar: ')
    if not BASE_URL.endswith('/'):
        BASE_URL += '/'

    for m in maps:
        plain = getKey(BASE_URL, header)
        upload(BASE_URL, header, maps[m], clientHash, plain, uid)


