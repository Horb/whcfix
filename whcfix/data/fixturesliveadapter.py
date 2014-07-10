import requests
import logging
from BeautifulSoup import BeautifulSoup
import datetime
import json
import os
import whcfix.utils as utils
from whcfix.data.adapterbase import AdapterBase


class FixturesLiveAdapter(AdapterBase):

    def __init__(self, fixLiveNumber, fixLiveName, clubName, sectionName):
        super(FixturesLiveAdapter, self).__init__(sectionName)
        self.fixLiveNumber = fixLiveNumber
        self.fixLiveName = fixLiveName
        self.clubName = clubName
        self.sectionName = sectionName

    def get_matches(self):
        dicts = self._get_match_dicts()
        return [self._getMatchObjectFromDict(d) for d in dicts]

    def _get_match_dicts_from_HTML(self, htmlString):
        soup = BeautifulSoup(htmlString)
        listOfMatches = []
        for tr in soup("tr"):
            matchDict = self._parse_row(tr)
            if matchDict is not None:
                listOfMatches.append(matchDict)
        return listOfMatches

    def _get_match_dicts(self):
        htmlString = self._get_HTML()
        return self._get_match_dicts_from_HTML(htmlString)

    def _parse_venue(self, venue_td):
        s = venue_td.text
        return " ".join(s.split(self.nbsp))

    def _get_HTML(self):
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
            if " " in date_time_td.text:
                date_fragment = date_time_td.text.split(" ")[0]
                return datetime.datetime.strptime(date_fragment, '%d.%m.%y')
            else:
                date_fragment = date_time_td.text
                return datetime.datetime.strptime(date_fragment, '%d.%m.%y')
        except ValueError as valErr:
            logging.exception("")
            return None
        except Exception as ex:
            logging.exception("")
            return None

    def _parse_time(self, date_time_td):
        try:
            if " " in date_time_td.text:
                date_fragment = date_time_td.text.split(" ")[1]
                return datetime.datetime.strptime(date_fragment, '%H:%M')
            return None
        except ValueError as valErr:
            logging.exception(date_time_td.text)
            return None
        except Exception as ex:
            logging.exception(date_time_td.text)
            return None

    def _parse_row(self, tr):
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
            return_me =  {'date':date, 'time':time, 'venue':venue, 
                          'home':home, 'homeGoals':homeGoals, 
                          'awayGoals':awayGoals, 'isPostponed':False, 'away':away}
            return return_me

        except Exception as ex:
            logging.exception("")
            return None


