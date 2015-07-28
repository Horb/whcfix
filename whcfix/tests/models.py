import logging
import unittest
from whcfix.logic.matches import Matches
from whcfix.logic.match import Match

# class Match(object):
#
#     def __init__(self, date, time, venue,
#                  home, homeGoals, awayGoals,
#                  away, isPostponed, section):


class MatchesTests(unittest.TestCase):

    def test_get_matches(self):
        _ = None
        m = Matches(auto_init_data=False)
        m1 = Match(_, _, _, _, _, _, _, _, _)
        m2 = Match(_, _, _, _, _, _, _, _, _)
        m3 = Match(_, _, _, _, _, _, _, _, _)
        m.listOfMatches = [m1, m2, m3]
        expected = [m1, m2, m3]
        actual = m.get_matches()
        self.assertEqual(expected, actual)

    def test_get_matches_team_feature_condition(self):
        _ = None
        m = Matches(auto_init_data=False)
        m1 = Match(_, _, _, "Team B", _, _, _, _, _)
        m2 = Match(_, _, _, "Team A", _, _, _, _, _)
        m3 = Match(_, _, _, "Team B", _, _, _, _, _)
        m.listOfMatches = [m1, m2, m3]
        expected = [m1, m3]
        actual = m.get_matches()
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
