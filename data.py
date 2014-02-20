import json

def initAppStrings():
    with open('/var/www/whcfix/strings.json') as jsonFile:
        return json.loads(jsonFile.read())

