import json


def getMaps():
    with open('Maps.json', 'r') as fin:
        parsed = json.loads(fin.read())
        maps = []
        for m in parsed:
            del parsed[m]['toBeat']
            maps.append(parsed[m])
    return maps


def getMapsForProfileTable():
    with open('Maps.json', 'r') as fin:
        parsed = json.loads(fin.read())
        maps = []
        for m in parsed:
            maps.append(ProfileMap(parsed[m]['MID'], parsed[m]['title'], parsed[m]['toBeat']))
        return maps


class ProfileMap:
    def __init__(self, id, title, toBeat):
        done = False
        score = 0
        self.id = id
        self.title = title
        self.toBeat = toBeat