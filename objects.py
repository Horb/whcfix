import datetime
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
                 home, homeGoals, awayGoals, away, isPostponed, section):
        self._date = date
        self._time = time
        self.venue = venue
        if section in home:
            self.home = home
        else:
            self.home = "%s %s" % (home, section)
        self.homeGoals = homeGoals
        self.awayGoals = awayGoals
        if section in away:
            self.away = away
        else:
            self.away = "%s %s" % (away, section)
        self.isPostponed = isPostponed

    def date_string(self):
        return self._date.strftime('%d-%m-%y') if isinstance(self._date, datetime.datetime) else ""
    
    def time_string(self):
        return self._time.strftime('%H:%M') if isinstance(self._time, datetime.datetime) else ""

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "%s %s - %s %s" % (self.home, self.homeGoals,
                                  self.awayGoals, self.away)

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
