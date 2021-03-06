import random
import string

from hashlib import pbkdf2_hmac
from Crypto.Cipher import AES

from bakand.db.dbClasses import User

BS = 16


def pad(s):
    return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)


def unpad(s):
    return s[0:-s[-1]]


def genKey(password):
    key = pbkdf2_hmac(
        hash_name='sha256',
        password=password,
        salt=b"pwnthem0le",
        iterations=65536,
        dklen=32
    )
    return key


def encrypt(data, key, user):
    iv = user.encode()
    data = pad(data)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(data.encode())


def decrypt(key, enc, user):
    iv = user.encode()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc))


def genPsw():
    return ''.join(
        random.SystemRandom().choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(20))


def createGuid():
    gid = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(16))
    while len(User.query.filter_by(guid=gid).all()) != 0:
        gid = ''.join(
            random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(16))
    return gid
