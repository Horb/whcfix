import requests
import logging
from BeautifulSoup import BeautifulSoup
import datetime
from whcfix.data.adapterbase import AdapterBase
from whcfix.logic.match import Match


nbsp = '&nbsp;'

def _getMatchObjectFromDict(matchDict, sectionName):
    date = matchDict['date']
    time = matchDict['time']
    venue = matchDict['venue']
    home = matchDict['home']
    homeGoals = matchDict['homeGoals']
    awayGoals = matchDict['awayGoals']
    isPostponed = matchDict['isPostponed']
    away = matchDict['away']
    return Match(date, time, venue, home, homeGoals, awayGoals, away,
                 isPostponed, sectionName)

def get_matches(sectionName, fixLiveNumber, club_name, league):
    dicts = _get_match_dicts(fixLiveNumber, club_name, league)
    return [_getMatchObjectFromDict(d, sectionName) for d in dicts]

def _get_match_dicts_from_HTML(htmlString, club_name, league):
    soup = BeautifulSoup(htmlString)
    listOfMatches = []
    for tr in soup("tr"):
        matchDict = _parse_row(tr, club_name, league)
        if matchDict is not None:
            listOfMatches.append(matchDict)
    return listOfMatches

def _get_match_dicts(fixLiveNumber, club_name, league):
    htmlString = _get_HTML(fixLiveNumber)
    return _get_match_dicts_from_HTML(htmlString, club_name, league)

def _parse_venue(venue_td):
    s = venue_td.text
    return " ".join(s.split(nbsp))

def _get_HTML(fixLiveNumber):
    url = 'http://w.fixtureslive.com/staticAPI.aspx?Operation=LoadData&a=team_view.ashx%3fteamid%3d' + str(fixLiveNumber)
    r = requests.get(url)
    return r.content

def _parse_home(home_td, team_td, club_name):
    if home_td.text == 'A':
        return team_td.text
    else:
        return club_name

def _parse_away(homeOrAwayIndicater, team_td, club_name):
    if homeOrAwayIndicater.text == 'A':
        return club_name
    else:
        return team_td.text

def _parse_homeGoals(score_td, home_away):
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

def _parse_awayGoals(score_td, home_away):
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

def _parse_date(date_time_td):
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

def _parse_time(date_time_td):
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

def _parse_row(tr, club_name, _league):
    logging.info("_parse_row")
    try:
        tds = tr("td")
        number_of_cells = len(tds)
        logging.info("expect 9 cells, number_of_cells=%s" % number_of_cells)
        if number_of_cells != 9:
            return None
        (_, oposition, _, score, league,
         date_time, home_away, venue, _) = tds
        if league.text != _league:
            return None
        home = _parse_home(home_away, oposition, club_name)
        homeGoals = _parse_homeGoals(score, home_away)
        away = _parse_away(home_away, oposition, club_name)
        awayGoals = _parse_awayGoals(score, home_away)
        date = _parse_date(date_time)
        time = _parse_time(date_time)
        venue = _parse_venue(venue)
        return_me = {'date': date, 'time': time, 'venue': venue,
                     'home': home, 'homeGoals': homeGoals,
                     'awayGoals': awayGoals, 'isPostponed': False,
                     'away': away}
        return return_me

    except Exception:
        logging.exception("")
        return None
