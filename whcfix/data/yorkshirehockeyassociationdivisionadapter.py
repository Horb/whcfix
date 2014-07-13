import requests
import logging
from BeautifulSoup import BeautifulSoup
import datetime
import json
import os
import whcfix.utils as utils
from whcfix.logic.division import Division, DivisionRow


class YorkshireHockeyAssociationDivisionAdapter(object):

    def __init__(self, leagueId, sectionName):
        self.leagueId = leagueId
        self.sectionName = sectionName

    def get_table_rows(self):
        for table_row in self._get_table_rows_from_HTML(self._get_HTML()):
            yield table_row
    
    def _get_HTML(self):
        url = "http://yorkshireha.org.uk/e107_plugins/league_manager/index.php?tables"
        payload = {
                "leagman_league_id":self.leagueId,
                }
        r = requests.post(url, data=payload)
        return r.content

    def _get_table_rows_from_HTML(self, html):
        soup = BeautifulSoup(html)
        list_of_table_rows = []
        for tr in soup("tr"):
            table_row = self._parse_row(tr)
            if table_row is not None:
                list_of_table_rows.append(table_row)
        return list_of_table_rows
    
    def _parse_row(self, tr):
        try:
            tds = tr("td")
            if len(tds) != 11:
                return None

            pos_td, team_td, played_td, won_td, drawn_td, lost_td, goals_for_td, goals_against_td, goals_difference_td, points_td, max_points_td = tds
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

            return_dict = {
                            "pos" : pos,
                            "team" : team,
                            "is_promotion" : is_promotion,
                            "is_relegation" : is_relegation,
                            "played" : played,  
                            "won" : won,
                            "drawn" : drawn,
                            "lost" : lost,
                            "goals_for" : goals_for,
                            "goals_against" : goals_against,
                            "goals_difference" : goals_difference,
                            "points" : points,
                            "max_points" : max_points,
                          }
            return return_dict
        except Exception as ex:
            logging.exception("")
            return None

    @utils.catch_log_return_None
    def _parse_int_from_td(self, td):
        return int(td.text)

    @utils.catch_log_return_None
    def _parse_team_td(self, team_td):
        return team_td.text

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


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)
    y = YorkshireHockeyAssociationDivisionAdapter(138, "Mens")
    print len([row for row in y.get_table_rows()])

