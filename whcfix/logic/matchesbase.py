import whcfix.settings as settings
from whcfix.data.yorkshirehockeyassociationadapter import YorkshireHockeyAssociationAdapter
from whcfix.data.fixturesliveadapter import FixturesLiveAdapter
from whcfix.data.picklecache import PickleCache

class MatchesBase(object):
    '''MatchBase handles initiating the class and making the data available.'''

    def __init__(self, auto_init_data=True):
        self.listOfMatches = []
        if auto_init_data:
            self.init_data()

    def init_data(self):
        pc = PickleCache('cache', 60 * 60)
        if pc.exists():
            self.listOfMatches = pc.load()
        else:
            for config in self.configGenerator():
                self.listOfMatches += self.getMatchesFromConfig(config)
            pc.dump(self.listOfMatches)

    def configGenerator(self):
        for config in self.getConfig()["configs"]:
            yield config

    def getConfig(self):
        return settings.CONFIGS

    def getMatchesFromConfig(self, config):
        if config['dataSource']['source'] == 'YorkshireHA':
            leagueId = config['dataSource']['league']
            clubId = config['dataSource']['club']
            sectionName = config['sectionName']
            adapter = YorkshireHockeyAssociationAdapter(leagueId, clubId, sectionName)
            return adapter.get_matches()
        elif config['dataSource']['source'] == 'FixturesLive':
            code = config['dataSource']['code']
            name = config['dataSource']['name']
            teamName = config['teamName']
            sectionName = config['sectionName']
            adapter = FixturesLiveAdapter(code, name, teamName, sectionName)
            return adapter.get_matches()
