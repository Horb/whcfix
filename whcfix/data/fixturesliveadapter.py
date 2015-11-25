import requests
import logging
from BeautifulSoup import BeautifulSoup
import datetime
from whcfix.data.adapterbase import AdapterBase


class FixturesLiveAdapter(AdapterBase):

    def __init__(self, fixLiveNumber, fixLiveName, clubName, sectionName):
        logging.info("FixturesLiveAdapter %s %s" % (fixLiveNumber, fixLiveNumber))
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
        url = 'http://w.fixtureslive.com/staticAPI.aspx?Operation=LoadData&a=team_view.ashx%3fteamid%3d' + str(self.fixLiveNumber)
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

    def _parse_homeGoals(self, score_td, home_away):
        if ":" in score_td.text:
            goals = score_td.text.split(":")
            goals = map(int, goals)
            if max(goals) == min(goals):
                # it's a draw, we cant return the wrong number of goals
                return goals[0]
            else:
                teamOfInterestGoals = goals[0]
                opositionGoals = goals[1]
                if "H" in home_away.text:
                    return teamOfInterestGoals
                elif "A" in home_away.text:
                    return opositionGoals
                else:
                    return None
        return None

    def _parse_awayGoals(self, score_td, home_away):
        if ":" in score_td.text:
            goals = score_td.text.split(":")
            goals = map(int, goals)
            if max(goals) == min(goals):
                # it's a draw, we cant return the wrong number of goals
                return min(goals)
            else:
                teamOfInterestGoals = goals[0]
                opositionGoals = goals[1]
                if "H" in home_away.text:
                    return opositionGoals
                elif "A" in home_away.text:
                    return teamOfInterestGoals
                else:
                    return None
        return None

    def _parse_date(self, date_time_td):
        try:
            if " " in date_time_td.text:
                date_fragment = date_time_td.text.split(" ")[0]
                return datetime.datetime.strptime(date_fragment, '%d.%m.%y')
            else:
                date_fragment = date_time_td.text
                return datetime.datetime.strptime(date_fragment, '%d.%m.%y')
        except ValueError:
            logging.exception("")
            return None
        except Exception:
            logging.exception("")
            return None

    def _parse_time(self, date_time_td):
        try:
            if " " in date_time_td.text:
                date_fragment = date_time_td.text.split(" ")[1]
                return datetime.datetime.strptime(date_fragment, '%H:%M')
            return None
        except ValueError:
            logging.exception(date_time_td.text)
            return None
        except Exception:
            logging.exception(date_time_td.text)
            return None

    def _parse_row(self, tr):
        logging.info("_parse_row")
        try:
            tds = tr("td")
            number_of_cells = len(tds)
            logging.info("expect 9 cells, number_of_cells=%s" % number_of_cells)
            if number_of_cells != 9:
                return None
            (_, oposition, _, score, league,
             date_time, home_away, venue, _) = tds
            home = self._parse_home(home_away, oposition)
            homeGoals = self._parse_homeGoals(score, home_away)
            away = self._parse_away(home_away, oposition)
            awayGoals = self._parse_awayGoals(score, home_away)
            date = self._parse_date(date_time)
            time = self._parse_time(date_time)
            venue = self._parse_venue(venue)
            return_me = {'date': date, 'time': time, 'venue': venue,
                         'home': home, 'homeGoals': homeGoals,
                         'awayGoals': awayGoals, 'isPostponed': False,
                         'away': away}
            return return_me

        except Exception:
            logging.exception("")
            return None
