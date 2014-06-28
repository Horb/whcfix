import datetime
import logging
import unittest
from whcfix.data.adapters import YorkshireHockeyAssociationAdapter
from whcfix.data.adapters import FixturesLiveAdapter
from BeautifulSoup import BeautifulSoup
import whcfix.settings as settings

class FixturesLiveAdapterTests(unittest.TestCase):

    def setUp(self):
        fixLiveNumber = None
        fixLiveName = None
        self.adapter = FixturesLiveAdapter(fixLiveNumber, fixLiveName, 
                                           'ClubName' , 'SectionName') 

    def test_parse_html(self):
        htmlString = ""
        with open('FixturesLiveExample1.html', 'r') as fl:
            for line in fl:
                htmlString += line
        match_dicts = self.adapter._get_match_dicts_from_HTML(htmlString)
        self.assertEqual(len(match_dicts), 22)
        homeSides = [m['home'] for m in match_dicts]
        awaySides = [m['away'] for m in match_dicts]
        sides = homeSides + awaySides
        sides = set(sides)
        self.assertTrue('ClubName' in sides)
        self.assertTrue("Harrogate Men's 1s" in sides)


    def test_parse_home(self):
        team_td = BeautifulSoup("<td>OppositionName</td>")
        home_td = BeautifulSoup("<td>H</td>")
        away_td = BeautifulSoup("<td>A</td>")
        expected = self.adapter.clubName
        actual = self.adapter._parse_home(home_td, team_td)
        self.assertEqual(actual, expected)
        expected = team_td.text
        actual = self.adapter._parse_home(away_td, team_td)
        self.assertEqual(actual, expected)

    def test_parse_away(self):
        team_td = BeautifulSoup("<td>OppositionName</td>")
        home_td = BeautifulSoup("<td>H</td>")
        away_td = BeautifulSoup("<td>A</td>")
        expected = team_td.text
        actual = self.adapter._parse_away(home_td, team_td)
        self.assertEqual(actual, expected)
        expected = self.adapter.clubName
        actual = self.adapter._parse_away(away_td, team_td)
        self.assertEqual(actual, expected)

    def test_parse_homeGoals(self):
        score_td = BeautifulSoup("<td>2:2</td>")
        indicatesWin = BeautifulSoup("<td>emerald</td>")
        indicatesLoss = BeautifulSoup("<td>red</td>")
        expected = 2
        actual = self.adapter._parse_homeGoals(score_td, None)
        self.assertEqual(actual, expected)

        score_td = BeautifulSoup("<td>3:2</td>")
        expected = 3
        actual = self.adapter._parse_homeGoals(score_td, indicatesWin)
        self.assertEqual(actual, expected)

        score_td = BeautifulSoup("<td>3:2</td>")
        expected = 2
        actual = self.adapter._parse_homeGoals(score_td, indicatesLoss)
        self.assertEqual(actual, expected)
