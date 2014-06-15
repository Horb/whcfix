import requests
import logging
from BeautifulSoup import BeautifulSoup
import datetime
import json
import whcfix.logic.objects as objects

def initAppStrings():
    with open('/home/adam/whcfix/whcfix/config/string.json') as jsonFile:
        return json.loads(jsonFile.read())


class AdapterBase(object):
    
    def __init__(self, sectionName):
        self.sectionName = sectionName
        self.nbsp = '&nbsp;'

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
        super(YorkshireHockeyAssociationAdapter, self).__init__(sectionName)
        self.leagueId = leagueId
        self.clubId = clubId
    
    def GetMatches(self):
        dicts = self._get_matches_from_HTML(self._get_HTML())
        return [self._getMatchObjectFromDict(d) for d in dicts]

    def _get_HTML(self):
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

    def _get_matches_from_HTML(self, html):
        soup = BeautifulSoup(html)
        listOfMatches = []
        for tr in soup("tr"):
            matchDict = self._parse_row(tr)
            if matchDict is not None:
                listOfMatches.append(matchDict)
        return listOfMatches
    
    def _parse_row(self, tr):
        try:
            tds = tr("td")
            if len(tds) != 6:
                return None
            date_td, time_td, venue_td, home_td, result_td, away_td = tds
            return {'date':self._parse_date(date_td),
                    'time':self._parse_time(time_td),
                    'venue':self._parse_venue(venue_td),
                    'home':self._parse_home(home_td),
                    'homeGoals':self._parse_homeGoals(result_td),
                    'awayGoals':self._parse_awayGoals(result_td),
                    'isPostponed':self._parse_isPostponed(result_td),
                    'away':self._parse_away(away_td)}
        except Exception as ex:
            return None


    def _parse_date(self, date_td):
        s = date_td.text
        try:
            return datetime.datetime.strptime(s, '%d %b %y')
        except Exception as ex:
            return None

    def _parse_time(self, time_td):
        s = time_td.text
        try:
            return datetime.datetime.strptime(s, '%H:%M')
        except Exception as ex: 
            return None

    def _parse_venue(self, venue_td):
        s = venue_td.text
        return " ".join(s.split(self.nbsp))

    def _parse_home(self, home_td):
        s = home_td.text
        return " ".join(s.split(self.nbsp))

    def _parse_away(self, away_td):
        s = away_td.text
        return " ".join(s.split(self.nbsp))

    def _parse_homeGoals(self, result_td):
        s = result_td.text
        if s == self.nbsp + self.nbsp:
            return None
        else:
            scores = s.split(self.nbsp)
            if 'P' in scores:
                return None
            else:
                return int(scores[0])

    def _parse_awayGoals(self, result_td):
        s = result_td.text
        if s == self.nbsp + self.nbsp:
            return None
        else:
            scores = s.split(self.nbsp)
            if 'P' in scores:
                return None
            else:
                return int(scores[1])

    def _parse_isPostponed(self, result_td):
        s = result_td.text
        if 'P' in s:
            return True
        else:
            return False

class FixturesLiveAdapter(AdapterBase):

    def __init__(self, fixLiveNumber, fixLiveName, clubName, sectionName):
        super(FixturesLiveAdapter, self).__init__(sectionName)
        self.fixLiveNumber = fixLiveNumber
        self.fixLiveName = fixLiveName
        self.clubName = clubName
        self.sectionName = sectionName

    def GetMatches(self):
        dicts = self._getMatchDicts()
        return [self._getMatchObjectFromDict(d) for d in dicts]

    def _getMatchDicts(self):
        htmlString = self._getHTML()
        soup = BeautifulSoup(htmlString)
        listOfMatches = []
        for tr in soup("tr"):
            matchDict = self._parse_row(tr)
            if matchDict is not None:
                listOfMatches.append(matchDict)
        return listOfMatches

    def _parse_venue(self, venue_td):
        s = venue_td.text
        return " ".join(s.split(self.nbsp))

    def _getHTML(self):
        url = "http://w.fixtureslive.com/team/%s/fixtures/%s"
        url = url % (self.fixLiveNumber, self.fixLiveName)
        r = requests.get(url)
        return r.content

    def _parse_home(self, home_td, team_td):
        if home_td.text == 'A':
            return team_td.text
        else:
            return self.clubName

    def _parse_away(self, homeOrAwayIndicater, team_td):
        if homeOrAwayIndicater.text == 'A':
            return self.clubName
        else:
            return team_td.text

    def _parse_homeGoals(self, score_td, resultIndicator):
        if ":" in score_td.text:
            goals = score_td.text.split(":")
            goals = map(int, goals)
            if max(goals) == min(goals):
                # it's a draw, we cant return the wrong number of goals
                return goals[0]
            else:
                if "emerald" in str(resultIndicator.text):
                    # this indicates a win for the club
                    return max(goals)
                else:
                    return min(goals)
        return None

    def _parse_awayGoals(self, score_td, resultIndicator):
        if ":" in score_td.text:
            goals = score_td.text.split(":")
            goals = map(int, goals)
            if max(goals) == min(goals):
                # it's a draw, we cant return the wrong number of goals
                return min(goals)
            else:
                if "emerald" in str(resultIndicator.text):
                    # this indicates a win for the club
                    return min(goals)
                else:
                    return max(goals)
        return None

    def _parse_date(self, date_time_td):
        try:
            date_fragment = date_time_td.text.split(" ")[0]
            return datetime.datetime.strptime(date_fragment, '%d.%m.%y')
        except ValueError as valErr:
            return None
        except Exception as ex:
            return None

    def _parse_time(self, date_time_td):
        try:
            date_fragment = date_time_td.text.split(" ")[1]
            return datetime.datetime.strptime(timeText, '%H:%M')
        except ValueError as valErr:
            return None
        except Exception as ex:
            return None

    def _parse_row(self, tr):
        logging.debug("Attempting to parse <tr>")
        try:
            if len(tr) != 9:
                return None
            _, oposition, resultIndicator, score, league, date_time, home_away, venue, _ = [child for child in tr.childGenerator()]
            home = self._parse_home(home_away, oposition)
            homeGoals = self._parse_homeGoals(score, resultIndicator)
            away = self._parse_away(home_away, oposition)
            awayGoals = self._parse_awayGoals(score, resultIndicator)
            date = self._parse_date(date_time)
            time = self._parse_time(date_time)
            venue = self._parse_venue(venue)
            return {'date':date,
                    'time':time,
                    'venue':venue,
                    'home':home,
                    'homeGoals':homeGoals,
                    'awayGoals':awayGoals,
                    'isPostponed':False,
                    'away':away}
        except Exception as ex:
            logging.warning("Exception whilst parsing <tr>: %s." % ex.message)
            return None


