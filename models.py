import adapters
import os
import json
import time
import pickle
import objects

class MatchesBase(object):
    '''MatchBase handles initiating the class and making the data available.'''

    def __init__(self):
        self.listOfMatches = []
        if self.cacheExists():
            self.loadFromCache()
        else:
            for config in self.configGenerator():
                self.listOfMatches += self.getMatchesFromConfig(config)
            self.saveToCache()

    def cacheExists(self):
        if os.path.exists('cache.pickle'):
            anHourInSeconds = 60 * 60
            ageOfCacheInSeconds = time.time() - os.path.getctime("cache.pickle")
            if  ageOfCacheInSeconds > anHourInSeconds:
                # The cache is out of date
                return False
            return True
        else:
            return False

    def saveToCache(self):
        with open('cache.pickle', 'w') as pickleFile:
            pickle.dump(self.listOfMatches, pickleFile)

    def loadFromCache(self):
        with open('cache.pickle') as pickleFile:
            self.listOfMatches = pickle.load(pickleFile)

    def configGenerator(self):
        for config in self.getConfig()["configs"]:
            yield config

    def getConfig(self):
        with open('config.json') as jsonFile:
            return json.loads(jsonFile.read())

    def getMatchesFromConfig(self, config):
        if config['dataSource']['source'] == 'YorkshireHA':
            leagueId = config['dataSource']['league']
            clubId = config['dataSource']['club']
            sectionName = config['sectionName']
            adapter = adapters.YorkshireHockeyAssociationAdapter(leagueId, clubId, sectionName)
            return adapter.getMatches()
        elif config['dataSource']['source'] == 'FixturesLive':
            code = config['dataSource']['code']
            name = config['dataSource']['name']
            teamName = config['teamName']
            sectionName = config['sectionName']
            adapter = adapters.FixturesLiveAdapter(code, name, teamName, sectionName)
            return adapter.getMatches()

class Matches(MatchesBase):

    def __init__(self):
        super(Matches, self).__init__()

    def all(self):
        return self.listOfMatches

    def filter(self, **kwargs):
        matches = []
        for match in self.listOfMatches:
            if self._filter(match, kwargs):
                matches.append(match)
        return matches

    def filterGen(self, **kwargs):
        for match in self.listOfMatches:
            if self._filter(match, kwargs):
                yield match

    def _filter(self, match, kwargs):
        for key, value in kwargs.iteritems():
            if match.__getattribute__(key) != value:
                return False
        else:
            return True

    def teamFilter(self, teamName):
        return [match 
                for match in self.listOfMatches 
                if match.doesFeature(teamName)]

    def lastFourResults(self, teamName):
        l = [match for match in self.listOfMatches
             if match.doesFeature(teamName) and match.isResult()]
        return l[len(l)-4:]

    def teamNames(self, teamNameFilter):
        awayNames = [match.away for match in self.listOfMatches if teamNameFilter in match.away]
        homeNames = [match.home for match in self.listOfMatches if teamNameFilter in match.home]
        names = awayNames + homeNames
        return set(names)

    def getLastResults(self, listOfTeamNames):
        def _lastResult(team):
            for match in self.listOfMatches[::-1]:
                if match.doesFeature(team) and match.isResult():
                    return match

        lastResults = []
        for team in listOfTeamNames:
            lastResults.append(_lastResult(team))
        return [match for match in lastResults if match is not None]

    def getNextMatches(self, listOfTeamNames):
        def _nextMatch(team):
            teamFixtures = [match for match in self.listOfMatches[::-1] if match.doesFeature(team)]
            for n, match in enumerate(teamFixtures):
                if match.isResult():
                    return teamFixtures[n-1]

        nextMatches = []
        for team in listOfTeamNames:
            nextMatches.append(_nextMatch(team))
        return nextMatches

    def recentForm(self, listOfTeamNames):
        def _getLastFourResults(name):
            results = []
            for match in self.listOfMatches[::-1]:
                if match.doesFeature(name) and match.isResult():
                    if match.didWin(name):
                        results.append(objects.Result('W', 'win', 3, match.teamGoalDifference(name)))
                    elif match.didLose(name):
                        results.append(objects.Result('L', 'lose', 0, match.teamGoalDifference(name)))
                    elif match.isDraw():
                        results.append(objects.Result('D', 'draw', 1, match.teamGoalDifference(name)))
                    else:
                        assert False
                if len(results) == 4:
                    print results
                    return results

        teams = [(_getLastFourResults(team), team) for team in listOfTeamNames]
        return [objects.TeamForm(name, results) for results, name in teams]

if __name__ == '__main__':
    m = Matches()
