import data
import objects

def appStrings():
    return data.initAppStrings()

def getMatchesObject():
    matches = []
    for config in data.getConfig()["configs"]:
        matches += getMatchesFromConfig(config)
    return objects.Matches(matches)

def getMatchesFromConfig(config):
    if config['dataSource']['source'] == 'YorkshireHA':
        leagueId = config['dataSource']['league']
        clubId = config['dataSource']['club']
        sectionName = config['sectionName']
        adapter = data.YorkshireHockeyAssociationAdapter(leagueId, clubId, sectionName)
        return adapter.getMatches()
    elif config['dataSource']['source'] == 'FixturesLive':
        code = config['dataSource']['code']
        name = config['dataSource']['name']
        teamName = config['teamName']
        sectionName = config['sectionName']
        adapter = data.FixturesLiveAdapter(code, name, teamName, sectionName)
        return adapter.getMatches()
