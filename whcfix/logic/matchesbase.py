import whcfix.settings as settings
import datetime
import os
import json
import time
import pickle
import logging
from whcfix.data.yorkshirehockeyassociationadapter import YorkshireHockeyAssociationAdapter
from whcfix.data.fixturesliveadapter import FixturesLiveAdapter

class MatchesBase(object):
    '''MatchBase handles initiating the class and making the data available.'''
    pathToCacheFile = os.path.join(os.getcwd(), 'cache.pickle')

    def __init__(self, auto_init_data=True):
        logging.debug(self.pathToCacheFile)
        self.listOfMatches = []
        if auto_init_data:
            self.init_data()

    def init_data(self):
        if self.cacheExists():
            self.loadFromCache()
        else:
            for config in self.configGenerator():
                self.listOfMatches += self.getMatchesFromConfig(config)
            self.saveToCache()

    def cacheExists(self):
        if os.path.exists(self.pathToCacheFile):
            anHourInSeconds = 59 * 60
            ageOfCacheInSeconds = time.time() - os.path.getctime(self.pathToCacheFile)
            if  ageOfCacheInSeconds > anHourInSeconds:
                # The cache is out of date
                return False
            return True
        else:
            return False

    def saveToCache(self):
        with open(self.pathToCacheFile, 'w') as pickleFile:
            pickle.dump(self.listOfMatches, pickleFile)

    def loadFromCache(self):
        with open(self.pathToCacheFile) as pickleFile:
            self.listOfMatches = pickle.load(pickleFile)

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
