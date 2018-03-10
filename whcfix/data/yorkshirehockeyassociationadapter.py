import datetime
import logging
import requests
from BeautifulSoup import BeautifulSoup
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
    if "Note" in matchDict:
        note = matchDict["Note"]
    else:
        note = ""
    return Match(date, time, venue, home, homeGoals, awayGoals, away,
                 isPostponed, sectionName, note)

# yorkshire_mens = get_matches("Mens", 204, home_away=1, club_id=66)
# yorkshire_ladies = get_matches("Ladies", 205, home_away=1, club_id=66)
# for m in yorkshire_mens + yorkshire_ladies:
#     m.date, m.home, m.away

def get_matches(sectionName, league_id, club_id="", date="all", division="", home_away="0"):
    html = _get_HTML(league_id, club_id, date, division, home_away)
    dicts = _get_match_dicts_from_HTML(html)
    return [_getMatchObjectFromDict(d, sectionName) for d in dicts]

def _get_HTML(league_id, club_id, date, division, home_away):
    url = "http://www.yorkshireha.org.uk/e107_plugins/league_manager/index.php?fixtures"
    payload = {
            "leagman_club": club_id, 
            "leagman_date": date,
            "leagman_division": division, 
            "leagman_fixtures_search_form": "1",
            "leagman_fixtures_search_form": "1", 
            "leagman_game": "0",
            "leagman_home_away": home_away,
            "leagman_league_id": league_id, 
            "leagman_team": "",
            "leagman_venue": "0"
            }
    r = requests.post(url,
                      headers={'user-agent': 'whcfix.com/1.0'},
                      data=payload)
    return r.text

def _get_match_dicts_from_HTML(html):
    soup = BeautifulSoup(html)
    listOfMatches = []
    for tr in soup("tr"):
        matchDict = _parse_row(tr)
        if matchDict is None:
            continue
        elif "Note" in matchDict and listOfMatches:
            listOfMatches[-1]["Note"] = matchDict["Note"]
        elif "date" in matchDict:
            listOfMatches.append(matchDict)
    return listOfMatches

def _parse_note(tds):
    try:
        return { "Note" : tds[0].text }
    except Exception:
        return None

def _parse_row(tr):
    try:
        tds = tr("td")
        if len(tds) == 2:
            return _parse_note(tds)
        if len(tds) != 6:
            return None
        date_td, time_td, venue_td, home_td, result_td, away_td = tds
        date = _parse_date(date_td)
        time = _parse_time(time_td)
        venue = _parse_venue(venue_td)
        home = _parse_home(home_td)
        homeGoals = _parse_homeGoals(result_td)
        awayGoals = _parse_awayGoals(result_td)
        isPostponed = _parse_isPostponed(result_td)
        away = _parse_away(away_td)

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

def _parse_date(date_td):
    try:
        return datetime.datetime.strptime(date_td.text, '%d %b %y')
    except Exception:
        logging.exception(date_td.text)
        return None

def _parse_time(time_td):
    try:
        if time_td.text == '--:--':
            return None
        return datetime.datetime.strptime(time_td.text, '%H:%M')
    except Exception:
        logging.exception(time_td.text)
        return None

def _parse_venue(venue_td):
    try:
        s = venue_td.text
        return " ".join(s.split(nbsp))
    except Exception:
        logging.exception(venue_td.text)
        return None

def _parse_home(home_td):
    try:
        s = home_td.text
        return " ".join(s.split(nbsp))
    except Exception:
        logging.exception(home_td.text)
        return None

def _parse_away(away_td):
    try:
        s = away_td.text
        return " ".join(s.split(nbsp))
    except Exception:
        logging.exception(away_td.text)
        return None

def _parse_homeGoals(result_td):
    try:
        s = result_td.text
        if s == nbsp + nbsp:
            return None
        else:
            scores = s.split(nbsp)
            if 'P' in scores:
                return None
            else:
                return int(scores[0])
    except Exception:
        logging.exception(result_td.text)
        return None

def _parse_awayGoals(result_td):
    try:
        s = result_td.text
        if s == nbsp + nbsp:
            return None
        else:
            scores = s.split(nbsp)
            if 'P' in scores:
                return None
            else:
                return int(scores[-1])
    except Exception:
        logging.exception(result_td.text)
        return None

def _parse_isPostponed(result_td):
    try:
        s = result_td.text
        if 'P' in s:
            return True
        else:
            return False
    except Exception:
        logging.exception(result_td.text)
        return False
