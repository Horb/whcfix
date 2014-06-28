import unittest
import logging
import datetime
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

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format=settings.LOG_FORMAT)
    unittest.main()

