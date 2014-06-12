import datetime
import unittest
from whcfix.data.adapters import YorkshireHockeyAssociationAdapter
from whcfix.data.adapters import FixturesLiveAdapter
from BeautifulSoup import BeautifulSoup

class FixturesLiveAdapterTests(unittest.TestCase):

    def setUp(self):
        fixLiveNumber = None
        fixLiveName = None
        self.adapter = FixturesLiveAdapter(fixLiveNumber, fixLiveName, 
                                           'ClubName' , 'SectionName') 

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


class YorkshireHockeyAssociationAdapterTests(unittest.TestCase):

    def setUp(self):
        self.adapter = YorkshireHockeyAssociationAdapter(None, None, None)

    def test_parse_row(self):
        html = '<tr>'
        html += '<td>27 Oct 14</td>'
        html += '<td>15:00</td>'
        html += '<td>Blue&nbsp;Pitch</td>'
        html += '<td>Blue&nbsp;Rovers</td>'
        html += '<td>1&nbsp;2</td>'
        html += '<td>Red&nbsp;Rovers</td>'
        html += '</tr>'
        tr = BeautifulSoup(html)
        actual = self.adapter._parse_row(tr)
        expected = {'date': datetime.datetime.strptime('27 Oct 14', '%d %b %y')
                    , 'time': datetime.datetime.strptime('15:00', '%H:%M')
                    , 'venue': 'Blue Pitch'
                    , 'home':'Blue Rovers'
                    , 'homeGoals':1
                    , 'awayGoals':2
                    , 'isPostponed':False
                    , 'away':'Red Rovers'
                    }
        self.assertEqual(actual, expected)

    def test_date_parsing(self):
        html = '<td>27 Oct 14</td>'
        date_td = BeautifulSoup(html)
        actual = self.adapter._parse_date(date_td)
        expected = datetime.datetime.strptime('27 Oct 14', '%d %b %y')
        self.assertEqual(actual, expected)

    def test_time_parsing(self):
        html = '<td>15:00</td>'
        time_td = BeautifulSoup(html)
        actual = self.adapter._parse_time(time_td)
        expected = datetime.datetime.strptime('15:00', '%H:%M')
        self.assertEqual(actual, expected)

    def test_postponed_result(self):
        html = '<td>P&nbsp;P</td>'
        result_td = BeautifulSoup(html)
        self.assertIsNone(self.adapter._parse_homeGoals(result_td))
        self.assertIsNone(self.adapter._parse_awayGoals(result_td))
        self.assertTrue(self.adapter._parse_isPostponed(result_td))

    def test_result_parsing(self):
        html = '<td>1&nbsp;2</td>'
        result_td = BeautifulSoup(html)
        self.assertEqual(1, self.adapter._parse_homeGoals(result_td))
        self.assertEqual(2, self.adapter._parse_awayGoals(result_td))
        self.assertFalse(self.adapter._parse_isPostponed(result_td))

    def test_home_parsing(self):
        html = '<td>Blue&nbsp;Rovers</td>'
        home_td = BeautifulSoup(html)
        self.assertEqual('Blue Rovers', self.adapter._parse_home(home_td))

    def test_away_parsing(self):
        html = '<td>Red&nbsp;Rovers</td>'
        away_td = BeautifulSoup(html)
        self.assertEqual('Red Rovers', self.adapter._parse_away(away_td))

    def test_venue_parsing(self):
        html = '<td>Blue&nbsp;Pitch</td>'
        venue_td = BeautifulSoup(html)
        self.assertEqual('Blue Pitch', self.adapter._parse_venue(venue_td))

if __name__ == '__main__':
    unittest.main()
