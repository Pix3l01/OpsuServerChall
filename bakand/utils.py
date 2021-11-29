import json


def getMaps():
    with open('Maps.json', 'r') as fin:
        parsed = json.loads(fin.read())
    return[parsed[map] for map in parsed]
