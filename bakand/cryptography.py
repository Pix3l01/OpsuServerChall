import random
import string

from hashlib import pbkdf2_hmac
from Crypto.Cipher import AES

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[0:-s[-1]]
chiavissima = ""


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
