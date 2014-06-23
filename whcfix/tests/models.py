import logging
import unittest
import whcfix.logic.models as models


class ModelBaseTests(unittest.TestCase):

    def test_init(self):
        base = models.MatchesBase()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()

