import unittest
import logging
from whcfix.data.yorkshirehockeyassociationdivisionadapter import YorkshireHockeyAssociationDivisionAdapter


class YHADivisionAdapterTests(unittest.TestCase):

    def test_main(self):
        a = YorkshireHockeyAssociationDivisionAdapter(138, "Mens")
        divisions = [d for d in a.get_divisions()]
        self.assertEqual(10, len(divisions))
        division_names = [d.name for d in divisions]
        self.assertTrue('Premier Division' in division_names)
        self.assertTrue('Division 2' in division_names)
        self.assertTrue('Division 3' in division_names)
        self.assertTrue('Division 4 North' in division_names)
        self.assertTrue('Division 4 South' in division_names)
        self.assertTrue('Division 5 North' in division_names)
        self.assertTrue('Division 5 South' in division_names)
        self.assertTrue('Division 6 North' in division_names)
        self.assertTrue('Division 6 South' in division_names)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()

