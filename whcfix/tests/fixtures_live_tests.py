import logging
import unittest
from whcfix.data.fixturesliveadapter import FixturesLiveAdapter
from BeautifulSoup import BeautifulSoup
import whcfix.settings as settings


class FixturesLiveAdapterTests(unittest.TestCase):

    def setUp(self):
        fixLiveNumber = None
        fixLiveName = None
        self.adapter = FixturesLiveAdapter(fixLiveNumber, fixLiveName,
                                           'ClubName', 'SectionName')

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

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format=settings.LOG_FORMAT)
    unittest.main()
