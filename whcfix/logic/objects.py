import datetime
import logging

class TeamForm(object):
    
    def __init__(self, teamName, results):
        self.results = results
        self.teamName = teamName

    def __int__(self):
        return self.points()

    def __gt__(self, other):
        if int(other) == int(self):
            return self.goalDifference() > other.goalDifference()
        else:
            return int(self) > int(other)

    def __lt__(self, other):
        if int(other) == int(self):
            return self.goalDifference() < other.goalDifference()
        else:
            return int(self) < int(other)

    def _countRecentResultInitial(self, initial):
        return len([r for r in self.results[:4] if r.resultInitial == initial])

    def wins(self):
        return self._countRecentResultInitial('W')

    def draws(self):
        return self._countRecentResultInitial('D')

    def loses(self):
        return self._countRecentResultInitial('L')

    def goalDifference(self):
        return sum([result.goalDifference for result in self.results])

    def points(self):
        return self.wins() * 3 + self.draws()

    def played(self):
        return len(self.results)


class Result(object):
    def __init__(self, resultInitial, resultIndicatorCssClass, points, goalDifference):
        self.resultInitial = resultInitial
        self.resultIndicatorCssClass = resultIndicatorCssClass
        self.points = points
        self.goalDifference = goalDifference


class Match(object):

    def __init__(self, date, time, venue, 
                 home, homeGoals, awayGoals, 
                 away, isPostponed, section):
        self._date = date
        self._time = time
        self._venue = venue
        if section in home:
            self._home = home
        else:
            self._home = "%s %s" % (home, section)
        self._homeGoals = homeGoals
        self._awayGoals = awayGoals
        if section in away:
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
    def venue(self):
        try:
            return self._venue
        except:
            return ""

    @property
    def isPostponed(self):
        try:
            return self._isPostponed
        except:
            return False

    @property
    def homeGoals(self):
        try:
            return self._homeGoals
        except:
            return 0

    @property
    def awayGoals(self):
        try:
            return self._awayGoals
        except:
            return 0

    @property
    def away(self):
        try:
            return self._away
        except:
            return ""

    @property
    def home(self):
        try:
            return self._home
        except:
            return ""
        
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
    def date(self):
        try:
            if self._date is None:
                return ""
            if isinstance(self._date, datetime.datetime):
                if self._date.year >= 1900:
                    return self._date.strftime('%d-%m-%y')
            return ""
        except:
            logging.critical("Couldn't format date as string.")
            return ""
    
    @property
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
        return self.homeGoals == None and self.awayGoals == None

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
        return self.homeGoals is not None and self.awayGoals is not None

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
