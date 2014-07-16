import logging
from whcfix.logic.teamform import TeamForm, Result
from whcfix.logic.matchesbase import MatchesBase


class Matches(MatchesBase):

    def __init__(self, auto_init_data=True):
        super(Matches, self).__init__(auto_init_data)

    def get_matches(self, condition=None):
        if condition == None:
            return self.listOfMatches
        else:
            return [m for m in self.listOfMatches if condition(m)]

    def lastFourResults(self, teamName):
        l = [match for match in self.listOfMatches
             if match.doesFeature(teamName) and match.isResult()]
        return l[len(l)-4:]

    def teamNames(self, teamNameFilter):
        names = []
        for match in self.listOfMatches:
            if match.home in names:
                continue
            else:
                if teamNameFilter in match.home:
                    names.append(match.home)
            if match.away in names:
                continue
            else:
                if teamNameFilter in match.away:
                    names.append(match.away)
        return names


    def lastResult(self, teamName):
        for match in self.listOfMatches[::-1]:
            if match.doesFeature(teamName) and match.isResult():
                return match
        return None

    def getLastResults(self, listOfTeamNames):
        lastResults = []
        for team in listOfTeamNames:
            lastResults.append(self.lastResult(team))
        return [match for match in lastResults if match is not None]

    def getNextMatches(self, listOfTeamNames):
        def _nextMatch(team):
            teamFixtures = [match for match in self.listOfMatches[::-1] if match.doesFeature(team)]
            for n, match in enumerate(teamFixtures):
                if match.isResult():
                    return teamFixtures[n-1]
            return match

        nextMatches = []
        for team in listOfTeamNames:
            nextMatches.append(_nextMatch(team))
        nextMatches.sort()
        nextMatches = [match 
                       for match in nextMatches 
                       if match is not None]
        nextMatches = [match 
                for match in nextMatches 
                if match.isMatchInTheFuture()]
        nextMatches = set(nextMatches)
        return nextMatches

    def recentForm(self, listOfTeamNames):
        def _getLastFourResults(name):
            results = []
            for match in self.listOfMatches[::-1]:
                if match.doesFeature(name) and match.isResult():
                    if match.didWin(name):
                        results.append(Result('W', 'win', 3, match.teamGoalDifference(name)))
                    elif match.didLose(name):
                        results.append(Result('L', 'lose', 0, match.teamGoalDifference(name)))
                    elif match.isDraw():
                        results.append(Result('D', 'draw', 1, match.teamGoalDifference(name)))
                    else:
                        assert False
                if len(results) == 4:
                    return results
        team_forms = []
        for team in listOfTeamNames:
            if len(self.get_matches(condition=lambda m: m.doesFeature(team) 
                                                    and m.isResult())) < 4:
                continue
            else:
                team_forms.append(TeamForm(team, _getLastFourResults(team)))
        return team_forms

if __name__ == '__main__':
    m = Matches()
