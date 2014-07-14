import unittest
import logging
from whcfix.logic.divisions import Divisions


class DivisionsModelTests(unittest.TestCase):

    def setUp(self):
        self.divisions = Divisions()

    def test_main(self):
        self.assertTrue(self.divisions.get_divisions() != [])

    def test_filter(self):
        condititon = lambda d: d.doesFeatureTeam("Wakefield 6 Mens")
        div6north = self.divisions.get_divisions(condititon)[0]
        self.assertEqual(div6north.name, 'Division 6 North')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
