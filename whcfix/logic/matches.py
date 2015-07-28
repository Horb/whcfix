import datetime
from whcfix.logic.teamform import TeamForm, Result
from whcfix.logic.matchesbase import MatchesBase


class Matches(MatchesBase):

    def __init__(self, auto_init_data=True):
        super(Matches, self).__init__(auto_init_data)

    def get_matches(self, condition=None):
        if condition is None:
            return self.listOfMatches
        else:
            return [m for m in self.listOfMatches if condition(m)]

    def lastFourResults(self, teamName):
        l = [match for match in self.listOfMatches
             if match.doesFeature(teamName) and match.isResult()]
        return l[len(l)-4:]

    def teamNames(self, teamNameFilter, section=None):
        names = []
        names = [m.home for m
                 in self.listOfMatches
                 if teamNameFilter in m.home]
        names += [m.away for m
                  in self.listOfMatches
                  if teamNameFilter in m.away]
        names = set(names)
        names = [n for n in names if section is None or section in n]
        names.sort()
        return names

    def getTodaysMatches(self, listOfTeamNames, section=None):
        todaysMatches = []
        today = datetime.date.today()
        for team in listOfTeamNames:
            if section is not None:
                if section not in team:
                    continue
            todaysMatches += [m for m in self.listOfMatches
                              if m.doesFeature(team)
                              and m._date.date() == today]
        todaysMatches.sort()
        return todaysMatches

    def lastResult(self, teamName):
        for match in self.listOfMatches[::-1]:
            if match.doesFeature(teamName) and match.isResult():
                return match
        return None

    def getLastResults(self, listOfTeamNames, section=None):
        lastResults = []
        for team in listOfTeamNames:
            if section is not None:
                if section not in team:
                    continue
            lastResult = self.lastResult(team)
            if lastResult is not None:
                lastResults.append(lastResult)
        lastResults.sort()
        return lastResults

    def nextMatch(self, team):
        teamFixtures = [m for m in self.listOfMatches
                        if m.doesFeature(team) and m.isMatchInTheFuture()]
        if teamFixtures:
            teamFixtures.sort()
            return teamFixtures[0]
        else:
            return None

    def getNextMatches(self, listOfTeamNames, section=None):
        nextMatches = []
        for team in listOfTeamNames:
            match = self.nextMatch(team)
            if match is not None and match not in nextMatches:
                nextMatches.append(match)
        if section is not None:
            nextMatches = [m for m in nextMatches
                           if section in m.home or section in m.away]
        nextMatches.sort()
        return nextMatches

    def recentForm(self, listOfTeamNames, section=None):
        def _getLastFourResults(name):
            results = []
            for match in self.listOfMatches[::-1]:
                if match.doesFeature(name) and match.isResult():
                    if match.didWin(name):
                        results.append(Result('W', 'win', 3,
                                       match.teamGoalDifference(name)))
                    elif match.didLose(name):
                        results.append(Result('L', 'lose', 0,
                                       match.teamGoalDifference(name)))
                    elif match.isDraw():
                        results.append(Result('D', 'draw', 1,
                                       match.teamGoalDifference(name)))
                    else:
                        assert False
                if len(results) == 4:
                    return results
        team_forms = []
        for team in listOfTeamNames:
            if section is not None:
                if section not in team:
                    continue
            c = lambda m: m.doesFeature(team) and m.isResult()
            if len(self.get_matches(condition=c)) < 4:
                continue
            else:
                team_forms.append(TeamForm(team, _getLastFourResults(team)))
        return team_forms

if __name__ == '__main__':
    m = Matches()
