import requests
import logging
from BeautifulSoup import BeautifulSoup
import whcfix.utils as utils
from whcfix.logic.division import Division, DivisionRow


class YorkshireHockeyAssociationDivisionAdapter(object):

    def __init__(self, leagueId, sectionName):
        self.leagueId = leagueId
        self.sectionName = sectionName

    def get_divisions(self):
        for d in self._get_divisions_from_HTML(self._get_HTML()):
            logging.debug("yielding division")
            yield d

    def _get_HTML(self):
        url = "http://yorkshireha.org.uk/e107_plugins/league_manager/index.php?tables"
        payload = {"leagman_league_id": self.leagueId}
        r = requests.post(url,
                          headers={'user-agent': 'whcfix.com/1.0'},
                          data=payload)
        return r.content

    def _get_divisions_from_HTML(self, html):
        soup = BeautifulSoup(html)
        division = None
        for tr in soup("tr"):
            division_name = self.try_parse_division_header(tr)
            if division_name is not None:
                if division is not None:
                    yield division
                logging.debug(division_name)
                division = Division("%s %s" % (self.sectionName,
                                               division_name))

            division_row = self.try_parse_division_row(tr)
            if division_row is not None:
                logging.debug("%s %s" % (division_row.pos, division_row.team))
                division.rows.append(division_row)
        if division is not None:
            yield division
        logging.debug(division_name)

    def try_parse_division_header(self, tr):
        try:
            ths = tr("th")
            if len(ths) != 10:
                return None
            name_th = ths[0]
            return name_th.text
        except:
            logging.exception("")
            return None

    def try_parse_division_row(self, tr):
        try:
            tds = tr("td")
            if len(tds) != 11:
                return None
            (pos_td, team_td, played_td, won_td, drawn_td, lost_td,
             goals_for_td, goals_against_td, goals_difference_td, points_td,
             max_points_td) = tds
            pos = self._parse_int_from_td(pos_td)
            is_promotion = self._parse_is_promotion(team_td)
            is_relegation = self._parse_is_relegation(team_td)
            team = self._parse_team_td(team_td)
            played = self._parse_int_from_td(played_td)
            won = self._parse_int_from_td(won_td)
            drawn = self._parse_int_from_td(drawn_td)
            lost = self._parse_int_from_td(lost_td)
            goals_for = self._parse_int_from_td(goals_for_td)
            goals_against = self._parse_int_from_td(goals_against_td)
            goals_difference = self._parse_int_from_td(goals_difference_td)
            points = self._parse_int_from_td(points_td)
            max_points = self._parse_int_from_td(max_points_td)
            return DivisionRow(pos, team, is_promotion, is_relegation, played,
                               won, drawn, lost, goals_for, goals_against,
                               goals_difference, points, max_points)
        except Exception:
            logging.exception("")
            return None

    @utils.catch_log_return_None
    def _parse_int_from_td(self, td):
        return int(td.text)

    @utils.catch_log_return_None
    def _parse_team_td(self, team_td):
        return "%s %s" % (team_td.text, self.sectionName)

    @utils.catch_log_return_None
    def _parse_is_promotion(self, team_td):
        if len(team_td("img")) == 0:
            return False
        img = team_td("img")[0]
        for attribute, value in img.attrs:
            if attribute == 'src' and "divup.gif" in value:
                return True
        return False

    @utils.catch_log_return_None
    def _parse_is_relegation(self, team_td):
        if len(team_td("img")) == 0:
            return False
        img = team_td("img")[0]
        for attribute, value in img.attrs:
            if attribute == 'src' and "divdown.gif" in value:
                return True
        return False
