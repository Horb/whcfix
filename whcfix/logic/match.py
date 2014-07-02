import datetime
import logging
import whcfix.utils as utils

class Match(object):

    def __init__(self, date, time, venue, 
                 home, homeGoals, awayGoals, 
                 away, isPostponed, section):
        self._date = date
        self._time = time
        self._venue = venue
        if home is not None:
            if section in home:
                self._home = home
            self._home = "%s %s" % (home, section)
        else:
            self._home = "%s %s" % (home, section)
        self._homeGoals = homeGoals
        self._awayGoals = awayGoals
        if away is not None and section in away:
            self._away = away
        else:
            self._away = "%s %s" % (away, section)
        self._isPostponed = isPostponed

    def isMatchInTheFuture(self):
        if self._date is None:
            return False
        if self._date > datetime.datetime.now():
            return True
        else:
            return False

    @property
    @utils.nz
    def venue(self):
        return self._venue

    @property
    def isPostponed(self):
        if self._isPostponed is None:
            return False
        else:
            return self._isPostponed

    @property
    @utils.nz
    def homeGoals(self):
        return self._homeGoals

    @property
    @utils.nz
    def awayGoals(self):
        return self._awayGoals

    @property
    @utils.nz
    def away(self):
        return self._away

    @property
    @utils.nz
    def home(self):
        return self._home
        
    def __gt__(self, other):
        try:
            if self._date != other._date:
                return self._date > other._date
            else:
                return self._time > other._time
        except:
            return False

    def __lt__(self, other):
        return not self.__gt__(other)

    @property
    @utils.nz
    def date(self):
        try:
            if self._date is None:
                return ""
            if isinstance(self._date, datetime.datetime):
                if self._date.year >= 1900:
                    return self._date.strftime('%d-%m-%y')
        except:
            logging.critical("Couldn't format date as string.")
            return ""
    
    @property
    @utils.nz
    def time(self):
        try:
            if self._time is None:
                return ""
            return self._time.strftime('%H:%M')
        except:
            logging.critical("Couldn't format time as string.")
            return ""

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "%s %s - %s %s" % (self.home, 
                                  self.homeGoals,
                                  self.awayGoals, 
                                  self.away)

    def isFixture(self):
        return self._homeGoals is None and self._awayGoals is None

    def isHomeWin(self):
        return self.homeGoals > self.awayGoals

    def isAwayWin(self):
        return self.homeGoals < self.awayGoals

    def isDraw(self):
        return self.homeGoals == self.awayGoals

    def didWin(self, teamName):
        if teamName == self.home:
            return self.isHomeWin()
        elif teamName == self.away:
            return self.isAwayWin()
        else:
            return False

    def doesFeature(self, teamName):
        return teamName == self.home or teamName == self.away

    def doesFeatureSearch(self, teamNameSubString):
        return teamNameSubString in self.home or teamNameSubString in self.away

    def didLose(self, teamName):
        return not self.didWin(teamName) and not self.isDraw()

    def isResult(self):
        return self._homeGoals is not None and self._awayGoals is not None

    def homeGoalDifference(self):
        if self.isResult():
            return self.homeGoals - self.awayGoals
        return 0

    def awayGoalDifference(self):
        if self.isResult():
            return self.awayGoals - self.homeGoals
        return 0

    def teamGoalDifference(self, teamName):
        if teamName == self.home:
            return self.homeGoalDifference()
        if teamName == self.away:
            return self.awayGoalDifference()
        else:
            0
