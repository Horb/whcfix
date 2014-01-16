import requests
from BeautifulSoup import BeautifulSoup
import json

def initAppStrings():
    with open('strings.json') as jsonFile:
        return json.loads(jsonFile.read())

def getConfig():
    with open('config.json') as jsonFile:
        return json.loads(jsonFile.read())

def getMatchesHTML(leagueId, clubId=0):
    url = "http://www.yorkshireha.org.uk/e107_plugins/league_manager/index.php?fixtures"
    payload = {
            "leagman_club":str(clubId),
            "leagman_date":"",
            "leagman_division":"",
            "leagman_fixtures_search_form":"1",
            "leagman_fixtures_search_form":"1",
            "leagman_game":"0",
            "leagman_home_away":"0,",
            "leagman_league_id":str(leagueId),
            "leagman_team":"",
            "leagman_venue":"0",
            }
    r = requests.post(url, data=payload)
    return r.content


def tryParseMatch(tr):
    tds = tr("td")
    nbsp = '&nbsp;'
    if len(tds) == 6:
        date, time, venue, home, result, away = tds
        date = date.text
        time = time.text
        venue = " ".join(venue.text.split(nbsp))
        home = " ".join(home.text.split(nbsp))
        if result.text == nbsp + nbsp:
            homeGoals = None
            awayGoals = None
        else:
            scores = result.text.split(nbsp)
            homeGoals = scores[0]
            awayGoals = scores[2]

        if homeGoals == u'P':
            homeGoals = None
            awayGoals = None
            isPostponed = True
        elif homeGoals != None:
            homeGoals = int(homeGoals)
            awayGoals = int(awayGoals)
            isPostponed = False
        else:
            isPostponed = False
        away = " ".join(away.text.split(nbsp))

        return {'date':date,
                'time':time,
                'venue':venue,
                'home':home,
                'homeGoals':homeGoals,
                'awayGoals':awayGoals,
                'isPostponed':isPostponed,
                'away':away}
    else:
        return None

def getMatchesJSON(leagueId, clubId=0):
    return json.dumps(getMatchDicts(leagueId, clubId))

def getMatchDicts(leagueId, clubId=0):
    htmlString = getMatchesHTML(leagueId, clubId)
    soup = BeautifulSoup(htmlString)
    listOfMatches = []
    for tr in soup("tr"):
        matchDict = tryParseMatch(tr)
        if matchDict is not None:
            listOfMatches.append(matchDict)
    return listOfMatches
