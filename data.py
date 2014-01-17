import requests
import objects
from BeautifulSoup import BeautifulSoup
import json
import pickle
import os
import time

def cacheExists():
    if os.path.exists('cache.pickle'):
        anHourInSeconds = 60 * 60
        ageOfCacheInSeconds = time.time() - os.path.getctime("cache.pickle")
        if  ageOfCacheInSeconds > anHourInSeconds:
            # Return false if the cache is out of date.
            return False
        return True
    else:
        return False

def cacheMatchesObject(matchesObject):
    with open('cache.pickle', 'w') as pickleFile:
        pickle.dump(matchesObject, pickleFile)

def getMatchesObjectFromCache():
    with open('cache.pickle') as pickleFile:
        return pickle.load(pickleFile)

def getConfig():
    with open('config.json') as jsonFile:
        return json.loads(jsonFile.read())

def initAppStrings():
    with open('strings.json') as jsonFile:
        return json.loads(jsonFile.read())

class AdapterBase():

    def _getHTML():
        raise Exception("Not Implimented")

    def _parseRow():
        raise Exception("Not Implimented")

    def _getMatchObjectFromDict(self, matchDict):
        date = matchDict['date']
        time = matchDict['time']
        venue = matchDict['venue']
        home = matchDict['home']
        homeGoals = matchDict['homeGoals']
        awayGoals = matchDict['awayGoals']
        isPostponed = matchDict['isPostponed']
        away = matchDict['away']
        return objects.Match(date, time, venue, 
                home, homeGoals, awayGoals, away,
                     isPostponed, self.sectionName)

class YorkshireHockeyAssociationAdapter(AdapterBase):

    def __init__(self, leagueId, clubId, sectionName):
        self.leagueId = leagueId
        self.clubId = clubId
        self.sectionName = sectionName
    
    def getMatches(self):
        dicts = self._getMatchDicts()
        return [self._getMatchObjectFromDict(d) for d in dicts]

    def _getMatchDicts(self):
        htmlString = self._getHTML()
        soup = BeautifulSoup(htmlString)
        listOfMatches = []
        for tr in soup("tr"):
            matchDict = self._parseRow(tr)
            if matchDict is not None:
                listOfMatches.append(matchDict)
        return listOfMatches

    def _getHTML(self):
        url = "http://www.yorkshireha.org.uk/e107_plugins/league_manager/index.php?fixtures"
        payload = {
                "leagman_club":self.clubId,
                "leagman_date":"",
                "leagman_division":"",
                "leagman_fixtures_search_form":"1",
                "leagman_fixtures_search_form":"1",
                "leagman_game":"0",
                "leagman_home_away":"0,",
                "leagman_league_id":self.leagueId,
                "leagman_team":"",
                "leagman_venue":"0",
                }
        r = requests.post(url, data=payload)
        return r.content

    def _parseRow(self, tr):
        try:
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
        except Exception as ex:
            print ex.message
            return None

class FixturesLiveAdapter(AdapterBase):

    def __init__(self, fixLiveNumber, fixLiveName, clubName, sectionName):
        self.fixLiveNumber = fixLiveNumber
        self.fixLiveName = fixLiveName
        self.clubName = clubName
        self.sectionName = sectionName

    def getMatches(self):
        dicts = self._getMatchDicts()
        return [self._getMatchObjectFromDict(d) for d in dicts]

    def _getMatchDicts(self):
        htmlString = self._getHTML()
        soup = BeautifulSoup(htmlString)
        listOfMatches = []
        for tr in soup("tr"):
            matchDict = self._parseRow(tr)
            if matchDict is not None:
                listOfMatches.append(matchDict)
        return listOfMatches

    def _getHTML(self):
        url = "http://w.fixtureslive.com/team/%s/fixtures/%s" % (self.fixLiveNumber, self.fixLiveName)
        r = requests.get(url)
        return r.content

    def _parseRow(self, tr):
        try:
            if len(tr) != 9:
                return None
            _, oposition, _, score, league, date_time, home_away, venue, _ = [child for child in tr.childGenerator()]
            if ":" in score.text:
                homeGoals, awayGoals = score.text.split(":")
                homeGoals, awayGoals = map(int, (homeGoals, awayGoals))
            elif score.text == "&nbsp;":
                homeGoals, awayGoals = None, None
            try:
                date, time = date_time.text.split(" ")
            except:
                date = date_time.text
                time = ""
            venue = venue.text
            if home_away.text == "A":
                home = oposition.text
                away = self.clubName
            else:
                home = self.clubName
                away = oposition.text
            return {'date':date,
                    'time':time,
                    'venue':venue,
                    'home':home,
                    'homeGoals':homeGoals,
                    'awayGoals':awayGoals,
                    'isPostponed':False,
                    'away':away}
        except Exception as ex:
            print ex.message
            return None
