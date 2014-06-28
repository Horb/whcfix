

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


