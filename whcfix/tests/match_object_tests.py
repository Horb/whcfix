import unittest
import logging
import datetime
from datetime import date, time
from whcfix.logic.match import Match
import whcfix.settings as settings

class MatchTests(unittest.TestCase):

    def test_that_display_fields_use_nz(self):
        ''' Create a match with aweful data but make sure the properties that
        we'll use in templates aren't every going to return None '''
        m = Match(None, None, None,
                  None, None, None,
                  None, None, None)
        self.assertFalse(m.venue is None)
        self.assertFalse(m.isPostponed is None)
        self.assertFalse(m.homeGoals is None)
        self.assertFalse(m.awayGoals is None)
        self.assertFalse(m.away is None)
        self.assertFalse(m.home is None)
        self.assertFalse(m.date is None)
        self.assertFalse(m.time is None)

    def test_is_match_in_the_future(self):
        date = datetime.datetime(2099, 03, 14)
        _ = None
        m = Match(date, _, _,
                  _, _, _,
                  _, _, _,)
        self.assertTrue(m.isMatchInTheFuture())

        date = datetime.datetime(1900, 03, 14)
        _ = None
        m = Match(date, _, _,
                  _, _, _,
                  _, _, _,)
        self.assertFalse(m.isMatchInTheFuture())

        m = Match(_, _, _,
                  _, _, _,
                  _, _, _,)
        self.assertFalse(m.isMatchInTheFuture())

    def test_isFixture_vs_isResult(self):
        _ = None
        fixture = Match(_, _, _,
                        _, _, _,
                        _, _, _)
        self.assertTrue(fixture.isFixture())
        self.assertFalse(fixture.isResult())

        result = Match(_, _, _,
                        _, 3, 2,
                        _, _, _)
        self.assertFalse(result.isFixture())
        self.assertTrue(result.isResult())

    def test_sorting1(self):
        m1 = Match(None, None, "Venue", 
                   "Home", 2, 1, "Away", 
                   False, "Mens")
        m2 = Match(None, None, "Venue", 
                   "Bome", 2, 1, "Away", 
                   False, "Mens")
        m3 = Match(None, None, "Venue", 
                   "Aome", 2, 1, "Away", 
                   False, "Mens")
        matches = [m1, m2, m3]
        matches.sort()
# When no time information is available, just use the home sides name
        self.assertEqual(matches[0].home, "Aome Mens")
        self.assertEqual(matches[1].home, "Bome Mens")
        self.assertEqual(matches[2].home, "Home Mens")
        

    def test_sorting2(self):
        m1 = Match(date(2014, 6, 1), time(15,30), "Venue", 
                   "Home", 2, 1, "Away", 
                   False, "Mens")
        m2 = Match(date(2014, 6, 1), time(12,30), "Venue", 
                   "Bome", 2, 1, "Away", 
                   False, "Mens")
        m3 = Match(date(2014, 6, 1), None, "Venue", 
                   "Aome", 2, 1, "Away", 
                   False, "Mens")
        matches = [m1, m2, m3]
        matches.sort()
# Nones come first
        self.assertEqual(matches[0].home, "Aome Mens")
        self.assertEqual(matches[1].home, "Bome Mens")
        self.assertEqual(matches[2].home, "Home Mens")


    def test_sorting3(self):
        m1 = Match(date(2014, 6, 8), time(15,30), "Venue", 
                   "Home", 2, 1, "Away", 
                   False, "Mens")
        m2 = Match(date(2014, 6, 2), time(12,30), "Venue", 
                   "Bome", 2, 1, "Away", 
                   False, "Mens")
        m3 = Match(date(2014, 6, 1), None, "Venue", 
                   "Aome", 2, 1, "Away", 
                   False, "Mens")
        matches = [m1, m2, m3]
        matches.sort()
# use dates to sort primarily
        self.assertEqual(matches[0].home, "Aome Mens")
        self.assertEqual(matches[1].home, "Bome Mens")
        self.assertEqual(matches[2].home, "Home Mens")

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format=settings.LOG_FORMAT)
    unittest.main()
