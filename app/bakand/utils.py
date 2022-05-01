import json
import os
import hashlib
import time

clientHash = None


def getMaps():
    with open('Maps.json', 'r') as fin:
        parsed = json.loads(fin.read())
        maps = []
        for m in parsed:
            del parsed[m]['toBeat']
            maps.append(parsed[m])
    return maps


def getMapsForProfileTable():
    # if os.path.isfile('../Maps.json'):
    #     print("C'è il file")
    # else:
    #     print("Non c'è il file")
    print(os.listdir('.'))
    with open('Maps.json', 'r') as fin:
        parsed = json.loads(fin.read())
        maps = []
        for m in parsed:
            maps.append(ProfileMap(parsed[m]['MID'], parsed[m]['title'], parsed[m]['toBeat']))
        return maps


def getClientHash():
    global clientHash
    if clientHash is None:
        with open("static/Client.jar", "rb") as f:
            b = f.read()  # read entire file as bytes
            clientHash = hashlib.sha256(b).hexdigest()
    print('New hash calculated')
    return clientHash, int(time.time())


class ProfileMap:
    def __init__(self, id, title, toBeat):
        done = False
        score = 0
        self.id = id
        self.title = title
        self.toBeat = toBeat
