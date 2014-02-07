import json

def initAppStrings():
    with open('strings.json') as jsonFile:
        return json.loads(jsonFile.read())

