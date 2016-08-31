import logging
import whcfix.settings as settings
import whcfix.data.yorkshirehockeyassociationadapter as yha
import whcfix.data.fixturesliveadapter as fl
from whcfix.data.picklecache import PickleCache


class MatchesBase(object):
    '''MatchBase handles initiating the class and making the data available.'''

    def __init__(self, config, auto_init_data=True):
        self.config = config
        self.listOfMatches = []
        try:
            if auto_init_data:
                self.init_data()
        except Exception:
            logging.exception("Failed to initialise MatchesBase.")

    def init_data(self):
        pc = PickleCache('cache', 60 * 60)
        if pc.exists():
            self.listOfMatches = pc.load()
        else:
            for config in self.configGenerator():
                self.listOfMatches += self.getMatchesFromConfig(config)
            pc.dump(self.listOfMatches)

    def configGenerator(self):
        for c in self.config["configs"]:
            yield c

    def getMatchesFromConfig(self, config):
        if config['dataSource']['source'] == 'YorkshireHA':
            leagueId = config['dataSource']['leagueId']
            clubId = config['dataSource']['clubId']
            sectionName = config['sectionName']
            return yha.get_matches(sectionName, leagueId)
        elif config['dataSource']['source'] == 'FixturesLive':
            sectionName = config['sectionName']
            fixLiveNumber = config['dataSource']['fixLiveNumber']
            club_name = config['dataSource']['club_name']
            league = config['dataSource']['league']
            return fl.get_matches(sectionName, fixLiveNumber, club_name, league)
