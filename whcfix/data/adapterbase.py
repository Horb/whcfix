from whcfix.logic.match import Match


class AdapterBase(object):

    def __init__(self, sectionName):
        self.sectionName = sectionName
        self.nbsp = '&nbsp;'

    def _get_HTML():
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
        return Match(date, time, venue, home, homeGoals, awayGoals, away,
                     isPostponed, self.sectionName)
