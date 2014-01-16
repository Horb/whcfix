import requests
from BeautifulSoup import BeautifulSoup
import json

def initAppStrings():
    with open('strings.json') as jsonFile:
        return json.loads(jsonFile.read())

def getConfig():
    with open('config.json') as jsonFile:
        return json.loads(jsonFile.read())


def getMatchesFixturesLive(teamNumber, teamName):
    url = "http://w.fixtureslive.com/team/%s/fixtures/%s" % (teamNumber, teamName)
    print url
    r = requests.get(url)
    return r.content

def tryParseMatchFixturesLive(htmlContent):
    soup = BeautifulSoup(htmlContent)
    teamName = "Wakefield 1s"
    for tr in soup("tr"):
        if len(tr) != 9:
            continue
        children = [child for child in tr.childGenerator()]
#            0 
#            1 Brooklands MU Men's 1s
#            2 
#            3 0:3
#            4 NPMHL MCN
#            5 14.09.13 16:30
#            6 A
#            7 BHC
#            8 Fixture ID: 1336350HistoryAdd to calendarAudit trailHow post-match details are addded
        _, oposition, _, score, league, date_time, home_away, venue, _ = children

        if ":" in score.text:
            homeGoals, awayGoals = score.text.split(":")
            homeGoals, awayGoals = map(int, (homeGoals, awayGoals))
        elif score.text == "&nbsp;":
            homeGoals, awayGoals = None, None

        date, time = date_time.text.split(" ")
        venue = venue.text
        if home_away.text == "A":
            home = oposition.text
            away = teamName
        else:
            home = teamName
            away = oposition.text

        yield {'date':date,
                'time':time,
                'venue':venue,
                'home':home,
                'homeGoals':homeGoals,
                'awayGoals':awayGoals,
                'away':away}
            

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

if __name__ == '__main__':
    content = getMatchesFixturesLive("1031", "Wakefield-Mens-1s")
    for match in tryParseMatchFixturesLive(content):
        print match
