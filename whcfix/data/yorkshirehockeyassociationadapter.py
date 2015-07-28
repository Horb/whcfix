import requests
import logging
from BeautifulSoup import BeautifulSoup
import datetime
from whcfix.data.adapterbase import AdapterBase


class YorkshireHockeyAssociationAdapter(AdapterBase):

    def __init__(self, leagueId, clubId, sectionName):
        super(YorkshireHockeyAssociationAdapter, self).__init__(sectionName)
        self.leagueId = leagueId
        self.clubId = clubId

    def get_matches(self):
        dicts = self._get_match_dicts_from_HTML(self._get_HTML())
        return [self._getMatchObjectFromDict(d) for d in dicts]

    def _get_HTML(self):
        url = "http://www.yorkshireha.org.uk/e107_plugins/league_manager/index.php?fixtures"
        payload = {"leagman_club": self.clubId, "leagman_date": "",
                   "leagman_division": "", "leagman_fixtures_search_form": "1",
                   "leagman_fixtures_search_form": "1", "leagman_game": "0",
                   "leagman_home_away": "0,",
                   "leagman_league_id": self.leagueId, "leagman_team": "",
                   "leagman_venue": "0"}
        r = requests.post(url,
                          headers={'user-agent': 'whcfix.com/1.0'},
                          data=payload)
        return r.content

    def _get_match_dicts_from_HTML(self, html):
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
            date = self._parse_date(date_td)
            time = self._parse_time(time_td)
            venue = self._parse_venue(venue_td)
            home = self._parse_home(home_td)
            homeGoals = self._parse_homeGoals(result_td)
            awayGoals = self._parse_awayGoals(result_td)
            isPostponed = self._parse_isPostponed(result_td)
            away = self._parse_away(away_td)

            return_dict = {'date': date,
                           'time': time,
                           'venue': venue,
                           'home': home,
                           'homeGoals': homeGoals,
                           'awayGoals': awayGoals,
                           'isPostponed': isPostponed,
                           'away': away}
            return return_dict
        except Exception:
            logging.exception("")
            return None

    def _parse_date(self, date_td):
        try:
            return datetime.datetime.strptime(date_td.text, '%d %b %y')
        except Exception:
            logging.exception(date_td.text)
            return None

    def _parse_time(self, time_td):
        try:
            if time_td.text == '--:--':
                return None
            return datetime.datetime.strptime(time_td.text, '%H:%M')
        except Exception:
            logging.exception(time_td.text)
            return None

    def _parse_venue(self, venue_td):
        try:
            s = venue_td.text
            return " ".join(s.split(self.nbsp))
        except Exception:
            logging.exception(venue_td.text)
            return None

    def _parse_home(self, home_td):
        try:
            s = home_td.text
            return " ".join(s.split(self.nbsp))
        except Exception:
            logging.exception(home_td.text)
            return None

    def _parse_away(self, away_td):
        try:
            s = away_td.text
            return " ".join(s.split(self.nbsp))
        except Exception:
            logging.exception(away_td.text)
            return None

    def _parse_homeGoals(self, result_td):
        try:
            s = result_td.text
            if s == self.nbsp + self.nbsp:
                return None
            else:
                scores = s.split(self.nbsp)
                if 'P' in scores:
                    return None
                else:
                    return int(scores[0])
        except Exception:
            logging.exception(result_td.text)
            return None

    def _parse_awayGoals(self, result_td):
        try:
            s = result_td.text
            if s == self.nbsp + self.nbsp:
                return None
            else:
                scores = s.split(self.nbsp)
                if 'P' in scores:
                    return None
                else:
                    return int(scores[-1])
        except Exception:
            logging.exception(result_td.text)
            return None

    def _parse_isPostponed(self, result_td):
        try:
            s = result_td.text
            if 'P' in s:
                return True
            else:
                return False
        except Exception:
            logging.exception(result_td.text)
            return False
