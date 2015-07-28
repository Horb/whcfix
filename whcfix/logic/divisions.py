import whcfix.settings as settings
from whcfix.data.yorkshirehockeyassociationdivisionadapter import YorkshireHockeyAssociationDivisionAdapter as YHADivAdapter
from whcfix.data.picklecache import PickleCache


class Divisions(object):

    def __init__(self):
        pc = PickleCache('yhadivisisons', 60*60)
        if pc.exists():
            self.divisions = pc.load()
        else:
            self.divisions = []
            for league_id, section_name in self.iAdapters():
                adapter = YHADivAdapter(league_id, section_name)
                for d in adapter.get_divisions():
                    self.divisions.append(d)
            pc.dump(self.divisions)

    def iAdapters(self):
        for config in settings.CONFIGS['configs']:
            if config['dataSource']['source'] == 'YorkshireHA':
                league_id = config['dataSource']['league']
                section_name = config['sectionName']
                yield league_id, section_name

    def get_divisions(self, condition=None):
        if condition is None:
            return self.divisions
        else:
            return [d for d in self.divisions if condition(d)]
