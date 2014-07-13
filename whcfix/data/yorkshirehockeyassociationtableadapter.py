import requests
import logging
from BeautifulSoup import BeautifulSoup
import datetime
import json
import os
import whcfix.utils as utils

def catch_log_return_None(func):
    def _catch_log_return_None(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            logging.exception("args: %s, kwargs %s" % (args, kwargs))
            return None
    return _catch_log_return_None


class TableRow(object):

    def __init__(self, pos, team, is_promotion, is_relegation, played, won, 
                 drawn, lost, goals_for, goals_against, goals_difference, 
                 points, max_points):
        self.pos = pos
        self.team = team
        self.is_promotion = is_promotion
        self.is_relegation = is_relegation
        self.played = played
        self.won = won
        self.drawn = drawn
        self.lost = lost
        self.goals_for = goals_for
        self.goals_against = goals_against
        self.goals_difference = goals_difference
        self.points = points
        self.max_points = max_points

        

class YorkshireHockeyAssociationTableAdapter(object):

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
            pos = self._parse_pos_td(pos_td)
            is_promotion = self._parse_is_promotion(team_td)
            is_relegation = self._parse_is_relegation(team_td)
            team = self._parse_team_td(team_td)
            played = self._parse_played_td(played_td)
            won = self._parse_won_td(won_td)
            drawn = self._parse_drawn_td(drawn_td)
            lost = self._parse_lost_td(lost_td)
            goals_for = self._parse_goals_for_td(goals_for_td)
            goals_against = self._parse_goals_against_td(goals_against_td)
            goals_difference = self._parse_goals_difference_td(goals_difference_td)
            points = self._parse_points_td(points_td)
            max_points = self._parse_max_points_td(max_points_td)
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

    @catch_log_return_None
    def _parse_pos_td(self, pos_td):
        return int(pos_td.text)

    @catch_log_return_None
    def _parse_team_td(self, team_td):
        return team_td.text

    @catch_log_return_None
    def _parse_is_promotion(self, team_td):
        if len(team_td("img")) == 0:
            return False
        img = team_td("img")[0]
        for attribute, value in img.attrs:
            if attribute == 'src' and "divup.gif" in value:
                return True
        return False

    @catch_log_return_None
    def _parse_is_relegation(self, team_td):
        if len(team_td("img")) == 0:
            return False
        img = team_td("img")[0]
        for attribute, value in img.attrs:
            if attribute == 'src' and "divdown.gif" in value:
                return True
        return False

    @catch_log_return_None
    def _parse_played_td(self, played_td):
        return int(played_td.text)

    @catch_log_return_None
    def _parse_won_td(self, won_td):
        return int(won_td.text)

    @catch_log_return_None
    def _parse_drawn_td(self, drawn_td):
        return int(drawn_td.text)

    @catch_log_return_None
    def _parse_lost_td(self, lost_td):
        return int(lost_td.text)

    @catch_log_return_None
    def _parse_goals_for_td(self, goals_for_td):
        return int(goals_for_td.text)

    @catch_log_return_None
    def _parse_goals_against_td(self, goals_against_td):
        return int(goals_against_td.text)

    @catch_log_return_None
    def _parse_goals_difference_td(self, td):
        return int(td.text)

    @catch_log_return_None
    def _parse_points_td(self, points_td):
        return int(points_td.text)

    @catch_log_return_None
    def _parse_max_points_td(self, max_points_td):
        return int(max_points_td.text)


if __name__ == '__main__':
    y = YorkshireHockeyAssociationTableAdapter(138, "Mens")
    print len([row for row in y.get_table_rows()])

